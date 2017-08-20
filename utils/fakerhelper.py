#encoding=utf-8
from faker import Faker
from faker.utils import text, decorators
from faker.utils.distribution import choice_distribution
from faker.providers import BaseProvider
import random

def GetRandomInt(start,end):
    data = random.randint(start, end)
    return data

def GetRandomFloat():
    # fake.pyfloat(left_digits=3)  right_digits
    fake = Faker()
    data = fake.pyfloat()
    return data

def GetFakerDataFromList(arr):
    '''arr = ('a', 'b', 'c', 'd') , choose one from list
    '''
    provider = BaseProvider(None)
    data = pick = provider.random_element(arr)
    return

def GetFakerDataAsPercent(arr,arrp):
    '''arr = ('a', 'b', 'c', 'd')
       arrp = (0.5, 0.2, 0.2, 0.1)
    '''
    data = choice_distribution(arr, arrp)
    return

def GetFakerData(seed=0,type="name"):
    # seed>0 : the same with last value
    fake = Faker()
    if seed > 0 :
        fake.seed(4321)
    if type=="useragent":
        fstr = fake.user_agent()
    if type=="password":
        #可以指定长度，也可以不指定
        len = GetRandomInt(8,13)
        password=fake.password(len)
    elif type=="name":
        fstr = fake.name()
    elif type=="email":
        fstr = fake.email()
    elif type=="address":
        fstr = fake.address()
    elif type=="company":
        fstr = fake.company()
    elif type=="job":
        fstr = fake.job()
    elif type=="phonenumber":
        fstr = fake.phone_number()
    elif type=="ssn":
        fstr = fake.ssn()
    elif type=="profile":
        fake.profile()
    elif type=="text":
        fstr = fake.text()
    elif type=="ipv4":
        fstr = fake.ipv4()
    elif type=="ipv6":
        fstr = fake.ipv6()
    elif type=="beforenow":
        fstr = fake.date_time_this_century(before_now=True, after_now=False)
    elif type=="afterrenow":
        fstr = fake.date_time_this_century(before_now=False, after_now=True)
    elif type=="beforenowthisyear":
        fstr = fake.date_time_this_year(before_now=True, after_now=False)
    elif type=="afterrenowthisyear":
        fstr = fake.date_time_this_year(before_now=False, after_now=True)
    elif type=="beforenowthismonth":
        fstr = fake.date_time_this_month(before_now=True, after_now=False)
    elif type=="afterrenowthismonth":
        fstr = fake.date_time_this_month(before_now=False, after_now=True)

    return fstr

def RemoveSlugify(str, allow_dots=False):
    #"a'b/c" => 'abc'
    slug = text.slugify("a'b/c",allow_dots=allow_dots)
    return slug
