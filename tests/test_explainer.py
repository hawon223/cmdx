from core.explainer import explain


def test_ls_explanation():

    result = explain("ls -al")

    assert "-a" in result
    assert "-l" in result