import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Nó do driver de joystick padrão do ROS 2 (lê de /dev/input/js0)
    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        parameters=[{
            'dev': '/dev/input/js0',
            'deadzone': 0.05,
            'autorepeat_rate': 20.0,
        }],
        output='screen'
    )

    # Nó customizado de tradução do controle para cmd_vel (serial_com_py)
    joystick_teleop_node = Node(
        package='serial_com_py',
        executable='joystick_teleop',
        name='joystick_teleop',
        parameters=[{
            'max_linear_speed': 0.15,  # m/s (Limite de velocidade solicitado)
            'max_angular_speed': 0.6,   # rad/s
            'axis_linear': 1,           # Analógico Esquerdo - Eixo Vertical
            'axis_angular': 0,          # Analógico Esquerdo - Eixo Horizontal
            'deadman_button': 4,        # Botão LB (Xbox 360) para segurança do robô
        }],
        output='screen'
    )

    return LaunchDescription([
        joy_node,
        joystick_teleop_node
    ])
