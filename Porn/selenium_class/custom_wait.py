# coding:utf-8

# 暂时没有用到了，留着参考用


class mp4_element_load_complete(object):

    def __call__(self, driver):
        element = driver.find_element_by_tag_name('source')
        text = element.get_attribute('type')
        if text == 'video/mp4':
            return element.get_attribute('src')
        else:
            return False
