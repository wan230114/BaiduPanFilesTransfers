from src.network import Network

EXP_MAP = {"1 天": 1, "7 天": 7, "30 天": 30, "永久": 0}


class share_baidu_link():

    def __init__(self, cookie, folder_name) -> None:
        self.cookie = cookie
        self.folder_name = folder_name
        self.network = Network()
        self.network.headers['Cookie'] = self.cookie
        self.var_expiry = self.expiry = "永久"  # 设置永久 
        self.var_password = self.password = "1234"  # 
        self.run()
    
    def run(self):
        self.handle_bdstoken()
        self.handle_list_dir()
        self.handle_process_share()

    def handle_bdstoken(self) -> None:
        """获取 bdstoken 相关逻辑"""
        self.network.bdstoken = self.network.get_bdstoken()
        if isinstance(self.network.bdstoken, int):
            print(f'没获取到 bdstoken 参数，错误代码：{self.network.bdstoken}')

    def handle_list_dir(self) -> None:
        """获取目标目录下的文件和目录列表"""
        self.dir_list_all = self.network.get_dir_list(f'/{self.folder_name}')
        if isinstance(self.dir_list_all, int) or not self.dir_list_all:
            print(f'目录 {self.folder_name} 中没获取到任何内容，请求返回：{self.dir_list_all}')

    def handle_process_share(self) -> None:
        """执行批量分享"""
        for info in self.dir_list_all:
            self.process_share(info)

    def process_share(self, info: dict) -> None:
        """执行分享操作并记录结果"""
        # 插入要分享的文件或文件夹到链接输入框，对文件夹加入 "/" 标记来区别
        is_dir = "/" if info["isdir"] == 1 else ""
        filename = f"{info['server_filename']}{is_dir}"
        msg = f'目录：{filename}' if is_dir else f'文件：{filename}'
        print(msg)

        # 发送创建分享请求
        r = self.network.create_share(info['fs_id'], EXP_MAP[self.expiry], self.password)
        if isinstance(r, str):
            result = f'链接：{r}?pwd={self.password}，密码：{self.password}，名称：{filename}'
        else:
            result = f'分享失败：错误代码（{r}），名称：{filename}'
        print(result)


CONFIG_PATH = "config.ini"
CONFIGs = [line.strip() for line in open(CONFIG_PATH).readlines()]

share_baidu_link(CONFIGs[0], CONFIGs[1])


