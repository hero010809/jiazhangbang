import os
import unittest
import HTMLTestRunner
import HTMLTestRunnerNew
import multiprocessing
import time
from util.write_user_command import WriteUserCommand
from business.mine_business import MineBusiness
from util.server import Server
from log.print_log import Log


class ParameTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest', parame=None):
        super(ParameTestCase, self).__init__(methodName)
        global parames
        parames = parame


class CaseTest(ParameTestCase):
    @classmethod
    def setUpClass(cls):
        print("setupclass----->", parames)
        cls.mine_business = MineBusiness(i)
        cls.driver = cls.mine_business.get_driver()

    @classmethod
    def tearDownClass(cls):
        print('this is class teardown')
        # cls.driver.quit()

    def setUp(self):
        self.logger = Log()
        self.logger.info("############################### START ###############################")

    def tearDown(self):
        self.logger.info('###############################  End  ###############################')
        for method_name, error in self._outcome.errors:
            if error:
                case_name = self._testMethodName
                file_name = os.getcwd().replace('case', 'result/screenshot/') + case_name + '.png'
                self.driver.save_screenshot(file_name)

    def test_01(self):
        '''成功进入搜索页面'''
        flag = self.mine_business.go_mine_pass()
        self.assertTrue(flag, msg="进入搜索页面测试不通过")


    def test_02(self):
        '''搜索功能模块的用例2'''
        self.search_business.search_pass()
        self.search_business.back()


def appium_init():
    server = Server()
    server.main()


def get_count():
    write_user_file = WriteUserCommand()
    count = write_user_file.get_file_lines()
    return count


def get_suite(i):
    print("get_suite里面的", i)
    suite = unittest.TestSuite()
    suite.addTest(CaseTest('test_01', parame=i))
    # suite.addTest(CaseTest('test_02', parame=i))
    # suite.addTest(CaseTest('test_03', parame=i))
    # suite.addTest(CaseTest('test_04', parame=i))
    # suite.addTest(CaseTest('test_05', parame=i))
    # suite.addTest(CaseTest('test_01'))
    # unittest.TextTestRunner().run(suite)

    now = time.strftime('%Y-%m-%d_%H_%M_%S')
    base_path = os.getcwd().replace('case', 'result/report/')
    file_path = base_path + now + str(i) + '.html'
    with open(file_path, 'wb') as f:
        # runner = HTMLTestRunner.HTMLTestRunner(stream=f, verbosity=2, title='自动化测试报告', description='xx')
        runner = HTMLTestRunnerNew.HTMLTestRunner(stream=f, verbosity=2, title='自动化测试报告', description='产品靠大家，质量你我他！',
                                                  tester='宋宵')
        runner.run(suite)


if __name__ == '__main__':
    appium_init()
    for i in range(get_count()):
        t = multiprocessing.Process(target=get_suite, args=(i,))
        t.start()