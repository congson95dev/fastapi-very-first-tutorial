# NOTE:
# this doesn't seem to work, only work with this case:
#
# my_func_1, my_func_2 contain this code: asyncio.sleep(5)
# features = [my_func_1(), my_func_2()]
# asyncio.gather(*features)


from fastapi import FastAPI
import time
import asyncio

app = FastAPI()


def run_func_without_async():
    result = []
    for i in range(2, 100000000):
        result.append(i)


async def run_func():
    result = []
    for i in range(2, 100000000):
        result.append(i)


async def my_func_1():
    print('Func1 started..!!')
    await run_func()
    print('Func1 ended..!!')

    return 'a..!!'


async def my_func_2():
    print('Func2 started..!!')
    await run_func()
    print('Func2 ended..!!')

    return 'b..!!'


@app.get("/home")
async def root():
    """
    my home route
    """
    start = time.time()

    a = run_func_without_async()
    b = run_func_without_async()

    end = time.time()

    print(start)
    print(end)
    print('It took {} seconds to finish execution.'.format(float(end) - float(start)))
    # result => 10 seconds

    start = time.time()

    a = await my_func_1()
    b = await my_func_2()

    end = time.time()

    print(start)
    print(end)
    print('It took {} seconds to finish execution.'.format(float(end) - float(start)))
    # result => 10 seconds

    start = time.time()

    # gather the function together and run them at the same time
    # add them to a list
    features = [my_func_1(), my_func_2()]
    # use the function asyncio.gather to run them at the same time
    a, b = await asyncio.gather(*features)

    end = time.time()

    print('It took {} seconds to finish execution.'.format(float(end) - float(start)))
    # result => 10 seconds

    return {
        'a': a,
        'b': b
    }
