# Press the green button in the gutter to run the script.

import nonebot as n
import config

if __name__ == '__main__':
    n.init(config)
    n.load_plugins("./Pinebot_main/plugins", "Pinebot_main.plugins")
    n.run(host = "127.0.0.1", port = 16241, debug = False)
    

# TODO: json读取列表等功能的整合