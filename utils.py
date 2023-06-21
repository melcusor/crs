def _preferences_dict_to_list(pref_dictionary):
    in_ent = []
    out_ent = []
    for k, v in pref_dictionary.items():
        if isinstance(v, dict):
            for k1, v1 in v.items():
                if k1 == "entities_in":
                    if isinstance(v1, list):
                        if v1:
                            in_ent = in_ent + v1
                else:
                    if v1:
                        out_ent = out_ent + v1
        else:
            in_ent = in_ent + v
    return in_ent, out_ent


def check_changes_in_preferences(old_dict, new_dict):
    #print("old_dict", old_dict)
    #print("new_dict", new_dict)

    old_in, old_out = _preferences_dict_to_list(old_dict)
    new_in, new_out = _preferences_dict_to_list(new_dict)

    #print("OLD: ")
    #print("in: ", old_in, "\nout: ", old_out)

    #print("NEW: ")
    #print("in: ", new_in, "\nout: ", new_out)

    differences_in_forth = set(old_in).difference(new_in)
    differences_in_back = set(new_in).difference(old_in)
    differences_out_forth = set(old_out).difference(new_out)
    differences_out_back = set(new_out).difference(old_out)

    #print("Diffs: ",
    #      set(new_in).difference(old_in) or set(old_in).difference(new_in) or set(new_out).difference(old_out) or set(
    #          old_out).difference(new_out))

    if differences_in_forth or differences_in_back or differences_out_forth or differences_out_back:
        #print("There are changes in preferences:")
        #print("Differences in forth: ", differences_in_forth)
        #print("Differences in back: ", differences_in_back)
        #print("Differences out forth: ", differences_out_forth)
        #print("Differences out back: ", differences_out_back)
        return True
    return False


def clean_recipe_title(named_entities_dict, recipe_title_dict):
    # get all entities out of the ne dictionary without recipe titles as list
    ne_in_list, ne_out_list = _preferences_dict_to_list(named_entities_dict)
    ne_list = ne_in_list + ne_out_list
    print("All entities: ", ne_list)

    # get all recipe titles as list
    title_in_list, title_out_list = _preferences_dict_to_list(recipe_title_dict)

    title_in_list = [y for x in title_in_list for y in x.split()]
    title_in_list = list(set(title_in_list) - set(ne_in_list))

    title_out_list = [y for x in title_out_list for y in x.split()]
    title_out_list = list(set(title_out_list) - set(ne_out_list))

    # print("CLEANED RECIPE TITLE - no other entities inside: ")
    # print("IN: ", title_in_list)
    # print("OUT: ", title_out_list)

    return {"entities_in": title_in_list, "entities_out": title_out_list}


def format_preferences_for_display(prefs_dictionary):
    prefs_in, prefs_out = _preferences_dict_to_list(prefs_dictionary)
    prefs_in = " | ".join(prefs_in)
    prefs_out = " | ".join(prefs_out)

    # return "entities_in: " + prefs_in + " | entities_out: " + prefs_out
    return {"entities_in": prefs_in,
            "entities_out": prefs_out}
