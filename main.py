from subprocess import run


class Module(object):
    def __get_list(self, pip_version: str = 'pip', encoding: str = 'utf-8') -> list:
        """
            アップデートが必要なファイルリストを取得して、ファイル名だけをlistにして返す。
        """
        check_command: str = f'sudo -H {pip_version} list --outdated'
        response: CompletedProcess = run(check_command.split(), check=True, capture_output=True)
        result = response.stdout.decode(encoding).split()

        if result:
            # テーブルヘッダ、ボーダーなどの不要な部分とバージョン部分をカットして返却している
            return result[4::2]
        else:
            raise UpdateNotFoundError

    def update(self, pip_version: str = 'pip', encoding: str = 'utf-8') -> None:
        try:
            lists: list = self.__get_list(pip_version=pip_version, encoding=encoding)
        except UpdateNotFoundError as e:
            print(e)
        else:
            update_command: str = 'sudo -H pip3.7 install -U'
            for i in lists:
                command: list = f"{update_command} {i}".split()
                response: CompletedProcess = run(command, check=False, capture_output=True)
                result: str = response.stdout.decode(encoding)
                print(result)
            print('全てのアップデート処理が完了しました...')


class UpdateNotFoundError(BaseException):
    def __str__(self):
        return 'アップデートが必要なpythonモジュールはありませんでした。'


if __name__ == '__main__':
    module = Module()
    try:
        module.update(pip_version='pip3.7', encoding='utf-8')
    except KeyboardInterrupt:
        print('ユーザによって処理が中断されました...')
    finally:
        print('全ての処理が完了しました...')
