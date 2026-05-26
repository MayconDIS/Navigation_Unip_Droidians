#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import select
import tty
import termios

msg = """
===================================================
Controle do Robô UD-H1 via Teclado (WASD)
===================================================
Comandos:
        [W]
   [A]  [S]  [D]

* W/S : Frente / Trás (0.2 m/s)
* A/D : Esquerda / Direita (0.6 rad/s)
* Espaço ou qualquer outra tecla : Parar o robô

Pressione CTRL+C para fechar.
===================================================
"""

def getKey(settings):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.05)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, settings)
    return key

class WASDTeleop(Node):
    def __init__(self):
        super().__init__('wasd_teleop')
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.speed = 0.2  # m/s
        self.turn = 0.6   # rad/s
        
        self.get_logger().info("Nó wasd_teleop carregado. Aguardando comandos do teclado...")

def main(args=None):
    rclpy.init(args=args)
    node = WASDTeleop()
    
    settings = termios.tcgetattr(sys.stdin)
    
    linear_vel = 0.0
    angular_vel = 0.0
    
    try:
        print(msg)
        while rclpy.ok():
            key = getKey(settings)
            
            if key != '':
                if key == 'w' or key == 'W':
                    linear_vel = node.speed
                    angular_vel = 0.0
                    print(f"\rComando: FRENTE (vel={linear_vel:.2f} m/s)             ", end="")
                elif key == 's' or key == 'S':
                    linear_vel = -node.speed
                    angular_vel = 0.0
                    print(f"\rComando: TRÁS (vel={linear_vel:.2f} m/s)             ", end="")
                elif key == 'a' or key == 'A':
                    # Mantém a velocidade linear atual para permitir curvar em movimento
                    angular_vel = node.turn
                    print(f"\rComando: CURVA ESQUERDA (vel={linear_vel:.2f} m/s, ang={angular_vel:.2f} rad/s)", end="")
                elif key == 'd' or key == 'D':
                    # Mantém a velocidade linear atual para permitir curvar em movimento
                    angular_vel = -node.turn
                    print(f"\rComando: CURVA DIREITA (vel={linear_vel:.2f} m/s, ang={angular_vel:.2f} rad/s) ", end="")
                elif key == ' ':
                    linear_vel = 0.0
                    angular_vel = 0.0
                    print(f"\rComando: PARAR (vel=0.0)                            ", end="")
                elif key == '\x03':  # CTRL+C
                    break
            
            twist = Twist()
            twist.linear.x = float(linear_vel)
            twist.angular.z = float(angular_vel)
            node.pub.publish(twist)
            
    except Exception as e:
        print(f"\nErro no teleop: {e}")
    finally:
        twist = Twist()
        node.pub.publish(twist)
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()
        print("\nWASD Teleop encerrado.")

if __name__ == '__main__':
    main()
