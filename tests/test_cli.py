from __future__ import annotations

from ai_redteam.cli import main


def test_cli_selects_single_test(capsys):
    exit_code = main(
        [
            "assess",
            "--target",
            "synthetic",
            "--tests",
            "PI-001",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Tests: 1" in captured.out
    assert "PI-001" in captured.out


def test_cli_selects_multiple_tests(capsys):
    exit_code = main(
        [
            "assess",
            "--target",
            "hardened",
            "--tests",
            "PI-001,TA-001,TA-002",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Tests: 3" in captured.out
    assert "PI-001" in captured.out
    assert "TA-001" in captured.out
    assert "TA-002" in captured.out


def test_cli_rejects_unknown_test(capsys):
    exit_code = main(
        [
            "assess",
            "--target",
            "synthetic",
            "--tests",
            "DOES-NOT-EXIST",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 2
    assert "Invalid test selection" in captured.out
    assert "DOES-NOT-EXIST" in captured.out


def test_cli_default_discovers_all_tests(capsys):
    exit_code = main(
        [
            "assess",
            "--target",
            "hardened",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Tests: 12" in captured.out
