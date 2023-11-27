def calculate_value(position, data):
    switch_dict = {
        "GK": calculate_sweeper_keeper_support(data, "GK"),
        "LB": calculate_wing_back_support(data, "LB"),
        "CB": calculate_ball_playing_defender_defend(data, "CB"),
        "RB": calculate_wing_back_support(data, "RB"),
        "CM": calculate_central_midfield(data, "CM"),
        "LW": calculate_inverted_winger_attack(data, "LW"),
        "RW": calculate_winger_attack(data, "RW"),
        "ST": calculate_striker(data, "ST"),
    }

    return switch_dict.get(position)


def calculate_sweeper_keeper_support(data, name):
    # Calculates GK -> Sweeper Keeper Support Score
    data['sks_key'] = (data['Agi'] + data['Ref'])
    data['sks_green'] = (
            data['Cmd'] + data['Kic'] + data['1v1'] + data['Ant'] +
            data['Cnt'] + data['Pos'])
    data['sks_blue'] = (
            data['Aer'] + data['Fir'] + data['Han'] + data['Pas'] +
            data['TRO'] + data['Dec'] + data['Vis'] + data['Acc'])
    data[name] = (((data['sks_key'] * 5) + (data['sks_green'] * 3) + (
            data['sks_blue'] * 1)) / 36).round(1)

    return data


def calculate_wing_back_support(data, name):
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
    data[name] = (((data['wbs_key'] * 5) + (data['wbs_green'] * 3) + (
            data['wbs_blue'] * 1)) / 47).round(1)

    return data


def calculate_ball_playing_defender_defend(data, name):
    # calculates Ball_playing_defender_Defend score
    data['bpdd_key'] = (
            data['Acc'] + data['Pac'] + data['Jum'] + data['Cmp'])
    data['bpdd_green'] = (
            data['Hea'] + data['Mar'] + data['Pas'] + data['Tck'] +
            data['Pos'] + data['Str'])
    data['bpdd_blue'] = (
            data['Fir'] + data['Tec'] + data['Agg'] + data['Ant'] +
            data['Bra'] + data['Cnt'] + data['Dec'] + data['Vis'])
    data[name] = (((data['bpdd_key'] * 5) + (data['bpdd_green'] * 3) + (
            data['bpdd_blue'] * 1)) / 46).round(1)
    return data


def calculate_central_midfield(data, name):
    data = calculate_box_to_box_midfielder_support(data, "CM BBM")
    data = calculate_deep_lying_playmaker_defend(data, "CM DLP")
    data[name] = ((data["CM BBM"] + data["CM DLP"]) / 2).round(1)
    return data


def calculate_box_to_box_midfielder_support(data, name):
    # calculates Box_to_box_midfielder_Support score
    data['b2bs_key'] = (
            data['Acc'] + data['Pac'] + data['Sta'] + data['Wor'])
    data['b2bs_green'] = (
            data['Pas'] + data['Tck'] + data['OtB'] + data['Tea'])
    data['b2bs_blue'] = (
            data['Dri'] + data['Fin'] + data['Fir'] + data['Lon'] +
            data['Tec'] + data['Agg'] + data['Ant'] + data['Cmp'] +
            data['Dec'] + data['Pos'] + data['Bal'] + data['Str'])
    data[name] = (((data['b2bs_key'] * 5) + (data['b2bs_green'] * 3) + (
            data['b2bs_blue'] * 1)) / 44).round(1)
    return data


def calculate_deep_lying_playmaker_defend(data, name):
    # calculates Deep_lying_playmaker_Defend score
    data['dlpd_key'] = (
            data['Wor'] + data['Sta'] + data['Acc'] + data['Pac'])
    data['dlpd_green'] = (
            data['Fir'] + data['Pas'] + data['Tec'] + data['Cmp'] +
            data['Dec'] + data['Tea'] + data['Vis'])
    data['dlpd_blue'] = (
            data['Tck'] + data['Ant'] + data['Pos'] + data['Bal'])
    data[name] = (((data['dlpd_key'] * 5) + (data['dlpd_green'] * 3) + (
            data['dlpd_blue'] * 1)) / 45).round(1)
    return data


def calculate_inverted_winger_attack(data, name):
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
    data[name] = (((data['iwa_key'] * 5) + (data['iwa_green'] * 3) + (
            data['iwa_blue'] * 1)) / 44).round(1)
    return data


def calculate_winger_attack(data, name):
    # calculates Winger_Attack score
    data['wa_key'] = (
            data['Acc'] + data['Pac'] + data['Sta'] + data['Wor'])
    data['wa_green'] = (
            data['Cro'] + data['Dri'] + data['Tec'] + data['Agi'])
    data['wa_blue'] = (
            data['Fir'] + data['Pas'] + data['Ant'] + data['Fla'] +
            data['OtB'] + data['Bal'])
    data[name] = (
            ((data['wa_key'] * 5) + (data['wa_green'] * 3) + (data['wa_blue'] * 1)) / 38).round(1)
    return data


def calculate_striker(data, name):
    data = calculate_pressing_forward_attack(data, "ST PF")
    data = calculate_advanced_forward_attack(data, "ST AF")
    data[name] = ((data["ST PF"] + data["ST AF"]) / 2).round(1)
    return data


def calculate_pressing_forward_attack(data, name):
    # calculates Pressing_forward_Attack score
    data['pfa_key'] = (data['Acc'] + data['Pac'] + data['Fin'])
    data['pfa_green'] = (
            data['Agg'] + data['Ant'] + data['Bra'] + data['OtB'] +
            data['Tea'] + data['Wor'] + data['Sta'])
    data['pfa_blue'] = (
            data['Fir'] + data['Cmp'] + data['Cnt'] + data['Dec'] +
            data['Agi'] + data['Bal'] + data['Str'])
    data[name] = (((data['pfa_key'] * 5) + (data['pfa_green'] * 3) + (
            data['pfa_blue'] * 1)) / 43).round(1)
    return data


def calculate_advanced_forward_attack(data, name):
    # calculates Advanced_forward_Attack score
    data['afa_key'] = (data['Acc'] + data['Pac'] + data['Fin'])
    data['afa_green'] = (
            data['Dri'] + data['Fir'] + data['Tec'] + data['Cmp'] +
            data['OtB'])
    data['afa_blue'] = (
            data['Pas'] + data['Ant'] + data['Dec'] + data['Wor'] +
            data['Agi'] + data['Bal'] + data['Sta'])
    data[name] = (((data['afa_key'] * 5) + (data['afa_green'] * 3) + (
            data['afa_blue'] * 1)) / 37).round(1)
    return data
