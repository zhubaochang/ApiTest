# linkface接口自动化测试

它包含功能:
  * 测试数据初始化，并对数据的插入做了封装。
  * unittest单元测试框架运行测试
  * HTMLTestRunner生成接口测试报告


Python版本与依赖库：
  * python3.5+ :https://www.python.org/
  * Requests : https://github.com/kennethreitz/requests
  * PyMySQL : https://github.com/PyMySQL/PyMySQL

框架说明：
  * interface路径下为python测试用例
  * excel_cases路径下为excel版本的测试用例
  * images路径下为用例所需的图片参数
  * report路径下为HTML格式的测试报告
  * result路径下为保存的CSV格式的接口调用返回
  * run.py为统一执行测试脚本的文件
