"""Token tests for the transfer function."""

import brownie
from brownie import accounts


def test_sender_balance_decreases(token):
    sender_balance = token.balanceOf(accounts[0])
    amount = sender_balance // 4

    token.transfer(accounts[1], amount, {"from": accounts[0]})

    assert token.balanceOf(accounts[0]) == sender_balance - amount


def test_receiver_balance_increases(token):
    receiver_balance = token.balanceOf(accounts[1])
    amount = token.balanceOf(accounts[0]) // 4

    token.transfer(accounts[1], amount, {"from": accounts[0]})

    assert token.balanceOf(accounts[1]) == receiver_balance + amount


def test_total_supply_not_affected(token):
    total_supply = token.totalSupply()
    amount = token.balanceOf(accounts[0])

    token.transfer(accounts[1], amount, {"from": accounts[0]})

    assert token.totalSupply() == total_supply


def test_returns_true(token):
    amount = token.balanceOf(accounts[0])
    tx = token.transfer(accounts[1], amount, {"from": accounts[0]})

    assert tx.return_value is True


def test_transfer_full_balance(token):
    amount = token.balanceOf(accounts[0])
    receiver_balance = token.balanceOf(accounts[1])

    token.transfer(accounts[1], amount, {"from": accounts[0]})

    assert token.balanceOf(accounts[0]) == 0
    assert token.balanceOf(accounts[1]) == receiver_balance + amount


def test_transfer_zero_tokens(token):
    sender_balance = token.balanceOf(accounts[0])
    receiver_balance = token.balanceOf(accounts[1])

    token.transfer(accounts[1], 0, {"from": accounts[0]})

    assert token.balanceOf(accounts[0]) == sender_balance
    assert token.balanceOf(accounts[1]) == receiver_balance


def test_transfer_to_self(token):
    sender_balance = token.balanceOf(accounts[0])
    amount = sender_balance // 4

    token.transfer(accounts[0], amount, {"from": accounts[0]})

    assert token.balanceOf(accounts[0]) == sender_balance


def test_insufficient_balance(token):
    balance = token.balanceOf(accounts[0])

    with brownie.reverts():
        token.transfer(accounts[1], balance + 1, {"from": accounts[0]})


def test_transfer_event_fires(token):
    amount = token.balanceOf(accounts[0])
    tx = token.transfer(accounts[1], amount, {"from": accounts[0]})

    assert len(tx.events) == 1
    assert tx.events["Transfer"].values() == [accounts[0], accounts[1], amount]
