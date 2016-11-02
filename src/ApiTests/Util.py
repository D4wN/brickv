##### Global Stuff
class Helper:
    HOST = "localhost"
    PORT = 4223
    UID = "3dfBkF" # FIXME change UID
    red = None
    ipcon = None

    @staticmethod
    def start_module(module_name):
        return Helper.red.vision_module_start(module_name)

    @staticmethod
    def kill_all_modules():
        return Helper.red.vision_remove_all_modules()

    @staticmethod
    def show_running_modules(module_name=None):
        ids = ""
        c = Helper.red.vision_libs_loaded_count()
        if c.result != 0:
            print "V.show_running_modules()::vision_libs_loaded_count"
            return
        for i in range(0, c.count):
            md_id = Helper.red.vision_module_get_id(i)
            if md_id.result != 0:
                # print "_button_debug_print_running_modules::vision_module_get_id"
                continue
            ids += str(md_id.id) + ","

        if module_name:
            print "[" + module_name + "] TV Running Modules = " + str(ids)
        else:
            print "TV Running Modules = " + str(ids)
