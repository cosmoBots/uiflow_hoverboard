
"""
file     HoverWheels
time     2025-03-14
author   Txinto Vaz
email   txinto@elporis.com
license  MIT License
"""

import machine

class HoverWheels:
    """
    note:
        en: ''
    details:
        color: '#c58ce4'
        link: https://github.com/cosmoBots/uiflow_hoverboard
        image: ''
        category: Custom
    example: ''
    """




    def __init__(self, uart_num, tx: int = 32, rx: int = 33):
        """
        label:
            en: '%1 init uart_num %2 tx %3 rx %4'
        params:
            uart_num:
                name: uart_num
                field: dropdown
                options:
                    '0': '0'
                    '1': '1'
                    '2': '2'
            tx:
                name: tx
                type: int
                default: '32'
                field: number
                max: '100'
                min: '0'
            rx:
                name: rx
                type: int
                default: '33'
                field: number
                max: '100'
                min: '0'
        """
        self.uart = machine.UART(uart_num, baudrate=115200, bits=8, parity=None, stop=1, tx=tx, rx=rx, timeout=0, timeout_char=0, invert=0, flow=0)

    def command(self, steer: int = 0, speed: int = 0):
        """
        label:
            en: command %1 steer %2 speed %3
        params:
            steer:
                name: steer
                type: int
                default: '0'
                field: number
                max: '100'
                min: '0'
            speed:
                name: speed
                type: int
                default: '0'
                field: number
                max: '100'
                min: '0'
        """
        start = 43981
        msg = bytearray(8)
        msg[0] = start & 255
        msg[1] = start >> 8
        msg[2] = steer & 255
        msg[3] = steer >> 8
        msg[4] = speed & 255
        msg[5] = speed >> 8
        checksum = (start ^ steer) ^ speed
        msg[6] = checksum & 255
        msg[7] = checksum >> 8
        self.uart.write(bytes(msg))

    def query(self, hover_data):
        """
        label:
            en: query %1 hover_data %2
        params:
            hover_data:
                name: hover_data
        """
        # Constantes
        hr_cte_start = 43981
        hr_st_inicio = 0
        hr_st_inicio_2 = 1
        hr_st_cmd1_1 = 2
        hr_st_cmd1_2 = 3
        hr_st_cmd2_1 = 4
        hr_st_cmd2_2 = 5
        hr_st_spd_r_1 = 6
        hr_st_spd_r_2 = 7
        hr_st_spd_l_1 = 8
        hr_st_spd_l_2 = 9
        hr_st_bat_1 = 10
        hr_st_bat_2 = 11
        hr_st_temp_1 = 12
        hr_st_temp_2 = 13
        hr_st_cmdled_1 = 14
        hr_st_cmdled_2 = 15
        hr_st_checksum_1 = 16
        hr_st_checksum_2 = 17

        # Estados y flags
        hr_msg_recibido = False
        hr_estado_recepcion = hr_st_inicio

        # Buffers y variables de decodificacion
        hr_byte_entrante = None
        hr_byte_anterior = None
        hr_msg_rcv = bytearray(32)

        # Valores intermedios de la recepcion
        hr_tmp_start = None
        hr_tmp_cmd1 = None
        hr_tmp_cmd2 = None
        hr_tmp_spd_r = None
        hr_tmp_spd_l = None
        hr_tmp_bat = None
        hr_tmp_temp = None
        hr_tmp_cmdled = None
        hr_tmp_checksum = None

        # Argumentos destino de la recepcion
        cmd1_flag = False
        cmd2_flag = False
        spd_r_flag = False
        spd_l_flag = False
        bat_flag = False
        temp_flag = False
        cmdled_flag = False

        while self.uart.any():
            hr_msg_rcv = self.uart.read(1)
            hr_byte_entrante = hr_msg_rcv[0]
            if hr_estado_recepcion==hr_st_inicio:
                hr_byte_anterior = hr_byte_entrante
                hr_estado_recepcion = hr_st_inicio_2

            elif hr_estado_recepcion==hr_st_inicio_2:
                start_entrante = (hr_byte_entrante << 8) | hr_byte_anterior
                if start_entrante == hr_cte_start:
                    hr_estado_recepcion = hr_st_cmd1_1

                else:
                    hr_estado_recepcion = hr_st_inicio

            elif hr_estado_recepcion==hr_st_cmd1_1:
                hr_byte_anterior = hr_byte_entrante
                hr_estado_recepcion = hr_st_cmd1_2

            elif hr_estado_recepcion==hr_st_cmd1_2:
                hr_tmp_cmd1 = (hr_byte_entrante << 8) | hr_byte_anterior
                hr_estado_recepcion = hr_st_cmd2_1

            elif hr_estado_recepcion==hr_st_cmd2_1:
                hr_byte_anterior = hr_byte_entrante
                hr_estado_recepcion = hr_st_cmd2_2

            elif hr_estado_recepcion==hr_st_cmd2_2:
                hr_tmp_cmd2 = (hr_byte_entrante << 8) | hr_byte_anterior
                hr_estado_recepcion = hr_st_spd_r_1

            elif hr_estado_recepcion==hr_st_spd_r_1:
                hr_byte_anterior = hr_byte_entrante
                hr_estado_recepcion = hr_st_spd_r_2

            elif hr_estado_recepcion==hr_st_spd_r_2:
                hr_tmp_spd_r = (hr_byte_entrante << 8) | hr_byte_anterior
                if hr_tmp_spd_r > 32000:
                    hr_tmp_spd_r = hr_tmp_spd_r - 65536

                hr_estado_recepcion = hr_st_spd_l_1

            elif hr_estado_recepcion==hr_st_spd_l_1:
                hr_byte_anterior = hr_byte_entrante
                hr_estado_recepcion = hr_st_spd_l_2

            elif hr_estado_recepcion==hr_st_spd_l_2:
                hr_tmp_spd_l = (hr_byte_entrante << 8) | hr_byte_anterior
                if hr_tmp_spd_l > 32000:
                    hr_tmp_spd_l = hr_tmp_spd_l - 65536

                hr_estado_recepcion = hr_st_bat_1

            elif hr_estado_recepcion==hr_st_bat_1:
                hr_byte_anterior = hr_byte_entrante
                hr_estado_recepcion = hr_st_bat_2

            elif hr_estado_recepcion==hr_st_bat_2:
                hr_tmp_bat = (hr_byte_entrante << 8) | hr_byte_anterior
                hr_estado_recepcion = hr_st_temp_1

            elif hr_estado_recepcion==hr_st_temp_1:
                hr_byte_anterior = hr_byte_entrante
                hr_estado_recepcion = hr_st_temp_2

            elif hr_estado_recepcion==hr_st_temp_2:
                hr_tmp_temp = (hr_byte_entrante << 8) | hr_byte_anterior
                hr_estado_recepcion = hr_st_cmdled_1

            elif hr_estado_recepcion==hr_st_cmdled_1:
                hr_byte_anterior = hr_byte_entrante
                hr_estado_recepcion = hr_st_cmdled_2

            elif hr_estado_recepcion==hr_st_cmdled_2:
                hr_tmp_cmdled = (hr_byte_entrante << 8) | hr_byte_anterior
                hr_estado_recepcion = hr_st_checksum_1

            elif hr_estado_recepcion==hr_st_checksum_1:
                hr_byte_anterior = hr_byte_entrante
                hr_estado_recepcion = hr_st_checksum_2

            elif hr_estado_recepcion==hr_st_checksum_2:
                hr_tmp_checksum = (hr_byte_entrante << 8) | hr_byte_anterior
                hr_estado_recepcion = hr_st_inicio
                hr_msg_recibido = True
                break

            else:
                pass

        if (hover_data != None and len(hover_data)>=7):
            cmd1_rcv = hover_data[0]
            cmd2_rcv = hover_data[1]
            spd_r_rcv = hover_data[2]
            spd_l_rcv = hover_data[3]
            bat_rcv = hover_data[4]
            temp_rcv = hover_data[5]
            cmdled_rcv = hover_data[6]

        else:
            cmd1_rcv = 0
            cmd2_rcv = 0
            spd_r_rcv = 0
            spd_l_rcv = 0
            bat_rcv = 0
            temp_rcv = 0
            cmdled_rcv = 0

        cmd1_flag = False
        cmd2_flag = False
        spd_r_flag = False
        spd_l_flag = False
        bat_flag = False
        temp_flag = False
        cmdled_flag = False

        if hr_msg_recibido:
            if cmd1_rcv != hr_tmp_cmd1:
                cmd1_rcv = hr_tmp_cmd1
                cmd1_flag = True

            if cmd2_rcv != hr_tmp_cmd2:
                cmd2_rcv = hr_tmp_cmd2
                cmd2_flag = True

            if spd_r_rcv != hr_tmp_spd_r:
                spd_r_rcv = hr_tmp_spd_r
                spd_r_flag = True

            if spd_l_rcv != hr_tmp_spd_l:
                spd_l_rcv = hr_tmp_spd_l
                spd_l_flag = True

            if bat_rcv != hr_tmp_bat:
                bat_rcv = hr_tmp_bat
                bat_flag = True

            if temp_rcv != hr_tmp_temp:
                temp_rcv = hr_tmp_temp
                temp_flag = True

            if cmdled_rcv != hr_tmp_cmdled:
                cmdled_rcv = hr_tmp_cmdled
                cmdled_flag = True

        return [cmd1_rcv, cmd2_rcv, spd_r_rcv, spd_l_rcv, bat_rcv, temp_rcv, cmdled_rcv,
        cmd1_flag, cmd2_flag, spd_r_flag, spd_l_flag, bat_flag, temp_flag, cmdled_flag]

    def changed_speed_r(self, hover_data):
        """
        label:
            en: speed_r_changed? %1 hover_data %2
        params:
            hover_data:
                name: hover_data
        """
        return hover_data[9]

    def decode_speed_r(self, hover_data):
        """
        label:
            en: decode_speed_r %1 hover_data %2
        params:
            hover_data:
                name: hover_data
        """
        return hover_data[2]

    def changed_speed_l(self, hover_data):
        """
        label:
            en: speed_l_changed? %1 hover_data %2
        params:
            hover_data:
                name: hover_data
        """
        return hover_data[10]

    def decode_speed_l(self, hover_data):
        """
        label:
            en: decode_speed_l %1 hover_data %2
        params:
            hover_data:
                name: hover_data
        """
        return hover_data[3]

    def changed_bat(self, hover_data):
        """
        label:
            en: bat_changed? %1 hover_data %2
        params:
            hover_data:
                name: hover_data
        """
        return hover_data[11]

    def decode_bat(self, hover_data):
        """
        label:
            en: decode_bat %1 hover_data %2
        params:
            hover_data:
                name: hover_data
        """
        return hover_data[4]

    def changed_temp(self, hover_data):
        """
        label:
            en: temp_changed? %1 hover_data %2
        params:
            hover_data:
                name: hover_data
        """
        return hover_data[12]

    def decode_temp(self, hover_data):
        """
        label:
            en: decode_temp %1 hover_data %2
        params:
            hover_data:
                name: hover_data
        """
        return hover_data[5]


