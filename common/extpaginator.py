from django.core.paginator import Paginator


class ExtPaginator(Paginator):
    # def __init__(self, object_list, per_page, range_num=5, orphans=0, allow_empty_first_page=True):

        #Paginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page)
    # def __init__(self, range_num=5):

    # range_num是指当前页码左右显示几个页码
    def __init__(self, object_list, per_page, range_num=5, orphans=0,
                 allow_empty_first_page=True):

        self.object_list = object_list
        self.per_page = int(per_page)
        self.orphans = int(orphans)
        self.allow_empty_first_page = allow_empty_first_page

        self.range_num = int(range_num)

    
    def page(self, number):
        """
        Returns a Page object for the given 1-based page number.
        """
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count

        # haha wocao
        self.page_num = number

        return self._get_page(self.object_list[bottom:top], number, self)

    @property 
    def page_range_ext(self):
        return self._page_range_ext()

    def _page_range_ext(self):
        num_count = 2 * self.range_num + 1

        if self.num_pages <= num_count:
            return range(1, self.num_pages + 1)
            
        num_list = []
        num_list.append(self.page_num)

        for i in range(1, self.range_num + 1):
            if self.page_num - i <= 0:
                num_list.append(num_count + self.page_num - i)
            else:
                num_list.append(self.page_num - i)
 
            if self.page_num + i <= self.num_pages:
                num_list.append(self.page_num + i)
            else:
                num_list.append(self.page_num + i - num_count)

        num_list.sort()

        return num_list