def calculate_value(position, data):
    switch_dict = {
        "gk": calculate_gk(data),
        "lb/rb": calculate_lb_rb(data),
        "cb": calculate_cb(data),
        "cm-bbm": calculate_cm_bbm(data),
        "cm-dlp": calculate_cm_dlp(data),
        "lw": calculate_lw(data),
        "rw": calculate_rw(data),
        "st-pf": calculate_st_pf(data),
        "st-af": calculate_st_af(data)
    }

    return switch_dict.get(position)

def calculate_gk(data):
    # Calculates GK -> Sweeper Keeper Support Score
    data['sks_key'] = (data['Agi'] + data['Ref'])
    data['sks_green'] = (
                data['Cmd'] + data['Kic'] + data['1v1'] + data['Ant'] +
                data['Cnt'] + data['Pos'])
    data['sks_blue'] = (
                data['Aer'] + data['Fir'] + data['Han'] + data['Pas'] +
                data['TRO'] + data['Dec'] + data['Vis'] + data['Acc'])
    data['gk'] = (((data['sks_key'] * 5) + (data['sks_green'] * 3) + (
                data['sks_blue'] * 1)) / 36)
    data.gk = data.gk.round(1)

    return data

def calculate_lb_rb(data):
    # calculates Wing_back_Support score
    data['wbs_key'] = (
                data['Acc'] + data['Pac'] + data['Sta'] + data['Wor'])
    data['wbs_green'] = (
                data['Cro'] + data['Dri'] + data['Mar'] + data['Tck'] +
                data['OtB'] + data['Tea'])
    data['wbs_blue'] = (
                data['Fir'] + data['Pas'] + data['Tec'] + data['Ant'] +
                data['Cnt'] + data['Dec'] + data['Pos'] + data['Agi'] +
                data['Bal'])
    data['lb_rb'] = (((data['wbs_key'] * 5) + (data['wbs_green'] * 3) + (
                data['wbs_blue'] * 1)) / 47)
    data.lb_rb = data.lb_rb.round(1)
    return data

def calculate_cb(data):
    # calculates Ball_playing_defender_Defend score
    data['bpdd_key'] = (
                data['Acc'] + data['Pac'] + data['Jum'] + data['Cmp'])
    data['bpdd_green'] = (
                data['Hea'] + data['Mar'] + data['Pas'] + data['Tck'] +
                data['Pos'] + data['Str'])
    data['bpdd_blue'] = (
                data['Fir'] + data['Tec'] + data['Agg'] + data['Ant'] +
                data['Bra'] + data['Cnt'] + data['Dec'] + data['Vis'])
    data['cb'] = (((data['bpdd_key'] * 5) + (data['bpdd_green'] * 3) + (
                data['bpdd_blue'] * 1)) / 46)
    data.cb = data.cb.round(1)
    return data

def calculate_cm_bbm(data):
    # calculates Box_to_box_midfielder_Support score
    data['b2bs_key'] = (
                data['Acc'] + data['Pac'] + data['Sta'] + data['Wor'])
    data['b2bs_green'] = (
                data['Pas'] + data['Tck'] + data['OtB'] + data['Tea'])
    data['b2bs_blue'] = (
                data['Dri'] + data['Fin'] + data['Fir'] + data['Lon'] +
                data['Tec'] + data['Agg'] + data['Ant'] + data['Cmp'] +
                data['Dec'] + data['Pos'] + data['Bal'] + data['Str'])
    data['cm_bbm'] = (((data['b2bs_key'] * 5) + (data['b2bs_green'] * 3) + (
                data['b2bs_blue'] * 1)) / 44)
    data.cm_bbm = data.cm_bbm.round(1)
    return data

def calculate_cm_dlp(data):
    # calculates Deep_lying_playmaker_Defend score
    data['dlpd_key'] = (
                data['Wor'] + data['Sta'] + data['Acc'] + data['Pac'])
    data['dlpd_green'] = (
                data['Fir'] + data['Pas'] + data['Tec'] + data['Cmp'] +
                data['Dec'] + data['Tea'] + data['Vis'])
    data['dlpd_blue'] = (
                data['Tck'] + data['Ant'] + data['Pos'] + data['Bal'])
    data['cm_dlp'] = (((data['dlpd_key'] * 5) + (data['dlpd_green'] * 3) + (
                data['dlpd_blue'] * 1)) / 45)
    data.cm_dlp = data.cm_dlp.round(1)

    return data

def calculate_lw(data):
    # calculates Inverted_winger_Attack score
    data['iwa_key'] = (
                data['Acc'] + data['Pac'] + data['Sta'] + data['Wor'])
    data['iwa_green'] = (
                data['Cro'] + data['Dri'] + data['Pas'] + data['Tec'] +
                data['Agi'])
    data['iwa_blue'] = (
                data['Fir'] + data['Lon'] + data['Ant'] + data['Cmp'] +
                data['Dec'] + data['Fla'] + data['OtB'] + data['Vis'] +
                data['Bal'])
    data['lw'] = (((data['iwa_key'] * 5) + (data['iwa_green'] * 3) + (
                data['iwa_blue'] * 1)) / 44)
    data.lw = data.lw.round(1)

    return data

def calculate_rw(data):
    # calculates Winger_Attack score
    data['wa_key'] = (
                data['Acc'] + data['Pac'] + data['Sta'] + data['Wor'])
    data['wa_green'] = (
                data['Cro'] + data['Dri'] + data['Tec'] + data['Agi'])
    data['wa_blue'] = (
                data['Fir'] + data['Pas'] + data['Ant'] + data['Fla'] +
                data['OtB'] + data['Bal'])
    data['rw'] = (
                ((data['wa_key'] * 5) + (data['wa_green'] * 3) + (data['wa_blue'] * 1)) / 38)
    data.rw = data.rw.round(1)

    return data

def calculate_st_pf(data):
    # calculates Pressing_forward_Attack score
    data['pfa_key'] = (data['Acc'] + data['Pac'] + data['Fin'])
    data['pfa_green'] = (
                data['Agg'] + data['Ant'] + data['Bra'] + data['OtB'] +
                data['Tea'] + data['Wor'] + data['Sta'])
    data['pfa_blue'] = (
                data['Fir'] + data['Cmp'] + data['Cnt'] + data['Dec'] +
                data['Agi'] + data['Bal'] + data['Str'])
    data['st_pf'] = (((data['pfa_key'] * 5) + (data['pfa_green'] * 3) + (
                data['pfa_blue'] * 1)) / 43)
    data.st_pf = data.st_pf.round(1)

    return data

def calculate_st_af(data):
    # calculates Advanced_forward_Attack score
    data['afa_key'] = (data['Acc'] + data['Pac'] + data['Fin'])
    data['afa_green'] = (
                data['Dri'] + data['Fir'] + data['Tec'] + data['Cmp'] +
                data['OtB'])
    data['afa_blue'] = (
                data['Pas'] + data['Ant'] + data['Dec'] + data['Wor'] +
                data['Agi'] + data['Bal'] + data['Sta'])
    data['st_af'] = (((data['afa_key'] * 5) + (data['afa_green'] * 3) + (
                data['afa_blue'] * 1)) / 37)
    data.st_af = data.st_af.round(1)
    
    return data