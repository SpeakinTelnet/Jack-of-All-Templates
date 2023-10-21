"""Token tests for the approval function."""

import pytest
from brownie import accounts


@pytest.mark.parametrize("idx", range(5))
def test_initial_approval_is_zero(token, idx):
    assert token.allowance(accounts[0], accounts[idx]) == 0


def test_approve(token):
    token.approve(accounts[1], 10**19, {"from": accounts[0]})

    assert token.allowance(accounts[0], accounts[1]) == 10**19


def test_modify_approve(token):
    token.approve(accounts[1], 10**19, {"from": accounts[0]})
    token.approve(accounts[1], 12345678, {"from": accounts[0]})

    assert token.allowance(accounts[0], accounts[1]) == 12345678


def test_revoke_approve(token):
    token.approve(accounts[1], 10**19, {"from": accounts[0]})
    token.approve(accounts[1], 0, {"from": accounts[0]})

    assert token.allowance(accounts[0], accounts[1]) == 0


def test_approve_self(token):
    token.approve(accounts[0], 10**19, {"from": accounts[0]})

    assert token.allowance(accounts[0], accounts[0]) == 10**19


def test_only_affects_target(token):
    token.approve(accounts[1], 10**19, {"from": accounts[0]})

    assert token.allowance(accounts[1], accounts[0]) == 0


def test_returns_true(token):
    tx = token.approve(accounts[1], 10**19, {"from": accounts[0]})

    assert tx.return_value is True


def test_approval_event_fires(token):
    tx = token.approve(accounts[1], 10**19, {"from": accounts[0]})

    assert len(tx.events) == 1
    assert tx.events["Approval"].values() == [accounts[0], accounts[1], 10**19]
