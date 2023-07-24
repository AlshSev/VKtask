import vk
import argparse

def load_settings(args):
    # Some defaults included
    settings = {
        "format" : "CSV",
        "path" : "report",
        "formatter_kwargs" : {}
    }

    # Settings from the file load first, 
    # so they are overwritten by command line arguments
    with open("settings.cfg") as f:
        for line in f:
            setting = line.split('=')
            settings[setting[0].strip()] = setting[1].strip()

    if args.token:
        settings["token"] = args.token
    if args.user:
        settings["user"] = args.user
    if args.format:
        settings["format"] = args.format
    if args.path:
        settings["path"] = args.path

    # Choose correct formatter
    settings["formatter"] = vk.get_formatter_by_ext(settings["format"])

    # Add some pretty printing for JSON
    if settings["format"] == "JSON":
        settings["formatter_kwargs"] = {
            "indent" : 4, # Basically pretty print JSON
            "ensure_ascii" : False # Display utf-8 chars in JSON
        }

    return settings

def setup_parser():
    parser = argparse.ArgumentParser(description=("Get friend list of"
                                                  " the given user"))

    parser.add_argument("--format", "-f", choices=['CSV', 'TSV', 'JSON'],
                        help="output file format")
    parser.add_argument("--path", "-p", help="output file path")
    parser.add_argument("--token", "-t", help="authorization token")
    parser.add_argument("--user", "-u", 
                        help="id of the user to grab friends from")
    parser.add_argument("--authorize", 
                        help="show OAuth link for authorization and exit", 
                        action="store_true")

    return parser

def get_arguments():
    parser = setup_parser()
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_arguments()

    if args.authorize:
        print(vk.get_auth_link())
        exit()

    settings = load_settings(args)
    friends = vk.get_all_friends(settings["user"], settings["token"])
    vk.dump_friends(friends, settings["path"], settings["formatter"],
                    **settings["formatter_kwargs"])
