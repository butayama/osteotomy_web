"""
Testing floating-point-numbers
Be careful - it's difficult!!!
Source: https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/
"""
import pytest
import app.Calculation as co
import sys

FLT_EPSILON = sys.float_info.epsilon


def almost_equal_relative(a, b, max_rel_diff=FLT_EPSILON):
    diff = abs(a - b)
    a = abs(a)
    b = abs(b)
    largest = max(a, b)
    return diff <= largest * max_rel_diff


@pytest.mark.skip
def test_input_real_loop(monkeypatch):
    min_n = -60
    max_n = 60
    responses = iter(["-63", "75", "12.1", "-0.45"])
    monkeypatch.setattr('builtins.input', lambda x: next(responses))
    with pytest.raises(ValueError) as excinfo:
        co.input_real_loop("coronal_component C in degrees = ", min_n, max_n)
    exception_msg = excinfo.value.args[0]
    assert exception_msg == f"only float in the range between {min_n} and {max_n} degrees are valid"
    with pytest.raises(ValueError) as excinfo:
        co.input_real_loop("coronal_component C in degrees = ", min_n, max_n)
    exception_msg = excinfo.value.args[0]
    assert exception_msg == f"only float in the range between {min_n} and {max_n} degrees are valid"
    assert co.input_real_loop("coronal_component C in degrees = ", min_n, max_n) == 12.1
    assert co.input_real_loop("coronal_component C in degrees = ", min_n, max_n) == -0.45


def test_calculate(monkeypatch):
    responses = iter(["27.1", "-8.2", "29.7", "13", "-19", "10"])
    monkeypatch.setattr('builtins.input', lambda x: next(responses))
    filename, c_a_d, s_a_d, t_a_d, c_a, s_a, t_a, a_tad, a_oa, a_azi, a_ele, a_aor = \
        co.CalculateAngles.calculate(27.1, -8.2, 29.7)
    assert filename == "result/single_cut_rotational_osteotomy_27.1_-8.2_29.7.txt"
    assert almost_equal_relative(c_a_d, 27.1)
    assert almost_equal_relative(s_a_d, -8.2)
    assert almost_equal_relative(t_a_d, 29.7)
    assert almost_equal_relative(c_a, 0.47298422729046335)
    assert almost_equal_relative(s_a, -0.143116998663535)
    assert almost_equal_relative(t_a, 0.5183627878423158)
    assert almost_equal_relative(a_tad, 0.488629044217534)
    assert almost_equal_relative(a_oa, -0.27449212933171835)
    assert almost_equal_relative(a_azi, 0.5336735232528763)
    assert almost_equal_relative(a_ele, 0.7715637424629385)
    assert almost_equal_relative(a_aor, 0.7085668037098172)

    filename, c_a_d, s_a_d, t_a_d, c_a, s_a, t_a, a_tad, a_oa, a_azi, a_ele, a_aor = \
        co.CalculateAngles.calculate(13.0, -19.0, 10.0)
    assert filename == "result/single_cut_rotational_osteotomy_13.0_-19.0_10.0.txt"
    assert almost_equal_relative(c_a_d, 13.0)
    assert almost_equal_relative(s_a_d, -19.0)
    assert almost_equal_relative(t_a_d, 10.0)
    assert almost_equal_relative(c_a, 0.22689280275926285)
    assert almost_equal_relative(s_a, -0.33161255787892263)
    assert almost_equal_relative(t_a, 0.17453292519943295)
    assert almost_equal_relative(a_tad, 0.3929964295500902)
    assert almost_equal_relative(a_oa, -0.9801515296175607)
    assert almost_equal_relative(a_azi, 1.067417992217277)
    assert almost_equal_relative(a_ele, 1.1581162298075764)
    assert almost_equal_relative(a_aor, 0.42955170427227857)
