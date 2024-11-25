import acp_times 
import arrow 
import supplement_tst
import nose 

START_TIME = arrow.get('2024-05-17 00:00:00', 'YYYY-MM-DD HH:mm:ss')

# My errors are in the form of a list
def test_negative_control(): 
    # print(f"MY DEBUG: acp_times.open_time(-1, 200, START_TIME) = {acp_times.open_time(-1, 200, START_TIME)}")
    assert isinstance(acp_times.open_time(-1, 200, START_TIME), list)
    assert isinstance(acp_times.close_time(-1, 200, START_TIME), list)
    assert acp_times.open_time(-1, 200, START_TIME)[0] == False
    assert acp_times.close_time(-1, 200, START_TIME)[0] == False

def test_open(): 
    arg11 = acp_times.open_time(0, 1000, START_TIME)
    arg12 = supplement_tst.calc_time_tst(0, 0, START_TIME)
    assert arg11 == arg12
    # print(f"MY DEBUG: arg11 = {arg11}, arg12 = {arg12}")
    arg21 = acp_times.open_time(200, 1000, START_TIME)
    arg22 = supplement_tst.calc_time_tst(5, 53, START_TIME)
    # print(f"MY DEBUG: acp_times.open_time(200, 1000, START_TIME) = {arg21}, " + 
    #       f"supplement_tst.calc_time_tst(5, 53, START_TIME) = {arg22}")
    assert arg21 == arg22
    assert acp_times.open_time(650, 1000, START_TIME) == \
            supplement_tst.calc_time_tst(20, 35, START_TIME)
    assert acp_times.open_time(990, 1000, START_TIME) == \
            supplement_tst.calc_time_tst(32, 44, START_TIME)
    assert acp_times.open_time(1000, 1000, START_TIME) == \
            supplement_tst.calc_time_tst(33, 5, START_TIME)

def test_close(): 
    assert acp_times.close_time(0, 1000, START_TIME) == \
            supplement_tst.calc_time_tst(0, 0, START_TIME)
    assert acp_times.close_time(200, 1000, START_TIME) == \
            supplement_tst.calc_time_tst(13, 20, START_TIME)
    assert acp_times.close_time(650, 1000, START_TIME) == \
            supplement_tst.calc_time_tst(44, 23, START_TIME)
    assert acp_times.close_time(990, 1000, START_TIME) == \
            supplement_tst.calc_time_tst(74, 8, START_TIME)
    assert acp_times.close_time(1000, 1000, START_TIME) == \
            supplement_tst.calc_time_tst(75, 0, START_TIME)
    
def test_20_percent():
    # Tuple is my error object containing error Boolean and message 
    assert isinstance(acp_times.open_time(1201, 1000, START_TIME), list)
    assert isinstance(acp_times.close_time(1201, 1000, START_TIME), list)

def test_within_20():
    assert acp_times.close_time(1200, 1000, START_TIME) == \
            supplement_tst.calc_time_tst(75, 0, START_TIME)
    assert acp_times.open_time(1200, 1000, START_TIME) == \
            supplement_tst.calc_time_tst(33, 5, START_TIME)


