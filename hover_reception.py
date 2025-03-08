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
hrarg_cmd1_flag_hrarg = False
hrarg_cmd2_flag_hrarg = False
hrarg_spd_r_flag_hrarg = False
hrarg_spd_l_flag_hrarg = False
hrarg_bat_flag_hrarg = False
hrarg_temp_flag_hrarg = False
hrarg_cmdled_flag_hrarg = False

while hrarg_hover_uart_hrarg.any():
    hr_msg_rcv = hrarg_hover_uart_hrarg.read(1)
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

if hr_msg_recibido:
    if hrarg_cmd1_rcv_hrarg != hr_tmp_cmd1:
        hrarg_cmd1_rcv_hrarg = hr_tmp_cmd1
        hrarg_cmd1_flag_hrarg = True

    if hrarg_cmd2_rcv_hrarg != hr_tmp_cmd2:
        hrarg_cmd2_rcv_hrarg = hr_tmp_cmd2
        hrarg_cmd2_flag_hrarg = True

    if hrarg_spd_r_rcv_hrarg != hr_tmp_spd_r:
        hrarg_spd_r_rcv_hrarg = hr_tmp_spd_r
        hrarg_spd_r_flag_hrarg = True

    if hrarg_spd_l_rcv_hrarg != hr_tmp_spd_l:
        hrarg_spd_l_rcv_hrarg = hr_tmp_spd_l
        hrarg_spd_l_flag_hrarg = True

    if hrarg_bat_rcv_hrarg != hr_tmp_bat:
        hrarg_bat_rcv_hrarg = hr_tmp_bat
        hrarg_bat_flag_hrarg = True

    if hrarg_temp_rcv_hrarg != hr_tmp_temp:
        hrarg_temp_rcv_hrarg = hr_tmp_temp
        hrarg_temp_flag_hrarg = True

    if hrarg_cmdled_rcv_hrarg != hr_tmp_cmdled:
        hrarg_cmdled_rcv_hrarg = hr_tmp_cmdled
        hrarg_cmdled_flag_hrarg = True

