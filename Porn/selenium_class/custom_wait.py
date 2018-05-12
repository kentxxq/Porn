# coding:utf-8


class mp4_element_load_complete(object):

    def __call__(self, driver):
        element = driver.find_element_by_tag_name('source')
        text = element.get_attribute('type')
        print(text)
        if text == 'video/mp4':
            return element.get_attribute('src')
        else:
            return False
