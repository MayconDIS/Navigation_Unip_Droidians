#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

class JoystickTeleop(Node):
    def __init__(self):
        super().__init__('joystick_teleop')
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.sub = self.create_subscription(Joy, 'joy', self.joy_callback, 10)
        
        # Parâmetros configuráveis
        self.declare_parameter('max_linear_speed', 0.15)  # m/s
        self.declare_parameter('max_angular_speed', 0.6)  # rad/s
        self.declare_parameter('axis_linear', 1)          # Eixo Y do Analógico Esquerdo (Frente/Trás)
        self.declare_parameter('axis_angular', 0)         # Eixo X do Analógico Esquerdo (Girar)
        self.declare_parameter('deadman_button', 4)       # Botão LB (Xbox 360) para segurança
        
        self.max_linear = self.get_parameter('max_linear_speed').value
        self.max_angular = self.get_parameter('max_angular_speed').value
        self.axis_linear = self.get_parameter('axis_linear').value
        self.axis_angular = self.get_parameter('axis_angular').value
        self.deadman_button = self.get_parameter('deadman_button').value
        
        self.get_logger().info(
            f"===================================================\n"
            f"Nó joystick_teleop carregado com sucesso!\n"
            f"Para mover o robô:\n"
            f"1. Mantenha pressionado o botão LB (Deadman Switch).\n"
            f"2. Utilize o Analógico Esquerdo (Frente/Trás e Girar).\n"
            f"Velocidade Linear Máx: {self.max_linear:.2f} m/s\n"
            f"Velocidade Angular Máx: {self.max_angular:.2f} rad/s\n"
            f"==================================================="
        )

    def joy_callback(self, msg: Joy):
        twist = Twist()
        
        # Verifica se o botão deadman (LB) está pressionado
        deadman_pressed = False
        if len(msg.buttons) > self.deadman_button:
            deadman_pressed = (msg.buttons[self.deadman_button] == 1)
        
        if deadman_pressed:
            # Obtém os valores dos eixos analógicos (-1.0 a 1.0)
            linear_axis_val = msg.axes[self.axis_linear] if len(msg.axes) > self.axis_linear else 0.0
            angular_axis_val = msg.axes[self.axis_angular] if len(msg.axes) > self.axis_angular else 0.0
            
            # Calcula velocidades com base nas velocidades máximas configuradas
            twist.linear.x = float(linear_axis_val * self.max_linear)
            twist.angular.z = float(angular_axis_val * self.max_angular)
            
            self.get_logger().info(
                f"Movendo: Linear={twist.linear.x:.2f} m/s, Angular={twist.angular.z:.2f} rad/s (LB Pressionado)",
                throttle_duration_sec=0.5
            )
        else:
            # Se soltar o botão de segurança, para imediatamente
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            
        self.pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = JoystickTeleop()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Nó joystick_teleop encerrado via interrupção do teclado.")
    finally:
        # Garante publicação de parada antes de encerrar
        twist = Twist()
        node.pub.publish(twist)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
