import vk

settings = {}
def load_settings():
    with open("settings.cfg") as f:
        for line in f:
            setting = line.split('=')
            settings[setting[0]] = setting[1]

if __name__ == "__main__":
    load_settings()
    friends = vk.get_all_friends(settings["user_id"], settings["token"])
    vk.dump_friends(friends)
    vk.dump_friends(friends, formatter=vk.tsv_formatter, 
                    filename="tsv_report", omit_header=True)
    vk.dump_friends(friends, formatter=vk.json_formatter, 
                    filename="json_report", omit_outer_key=False, 
                    ensure_ascii=False, indent=4)