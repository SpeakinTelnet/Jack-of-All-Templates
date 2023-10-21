"""Deployment script for the Token Contract."""
import os

import solcx
from dotenv import load_dotenv
from eth_account import Account
from web3 import Web3
from web3.contract import Contract
from web3.types import TxParams

###################     FILL ME     ########################
CONTRACT_NAME: str = "Token"
CONTRACT_PATH: str = "contracts/Token.sol"
CONTRACT_VERSION: str = "^0.6.0"
CONSTRUCTOR_ARGS: tuple = ("Test Token", "TST", 18, int(1e21))
############################################################


load_dotenv()


http_addr = os.getenv("HTTP_PROVIDER")
_eth_account_private_key = os.getenv("ETH_PRIVATE_KEY")

solcx.install_solc("0.6.0")

w3 = Web3(Web3.HTTPProvider(http_addr))
eth_account: Account = Account.from_key(_eth_account_private_key)

last_block = w3.eth.get_block("latest", full_transactions=True)

max_fee_per_gas = last_block["baseFeePerGas"]


def get_precompile_contract() -> Contract:
    """Create a web3 contract instance from a compiled contract's ABI and Bytecode.

    Compile a temporary contract using the .sol file and use its ABI and Bytecode to
    create a reusable Web3 contract instance

    Returns
    -------
    Contract
        reusable Web3 contract instance
    """
    temp_file = solcx.compile_files(
        [CONTRACT_PATH],
        output_values=["abi", "bin"],
        solc_version="0.6.0",
    )
    abi = temp_file[f"{CONTRACT_PATH}:{CONTRACT_NAME}"]["abi"]
    bytecode = temp_file[f"{CONTRACT_PATH}:{CONTRACT_NAME}"]["bin"]
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    return contract


def create_contract_transaction(
    contract: Contract, *constructor_args: tuple
) -> tuple[TxParams, int]:
    """Create an unsigned transaction to deploy the provided contract.

    Parameters
    ----------
    contract : Contract
        reusable Web3 contract instance

    constructor_args : tuple[str]
        tuple of all the arguments used to deploy the contract

    Returns
    -------
    tuple[TxParams, int]
        Transaction attributes as TxParams and estimated gas usage of the transaction
    """
    constructor = contract.constructor(*constructor_args)
    gas = constructor.estimate_gas({"from": eth_account.address})
    construct_txn = contract.constructor(*CONSTRUCTOR_ARGS).build_transaction(
        {
            "maxPriorityFeePerGas": 1,
            "maxFeePerGas": max_fee_per_gas,
            "gas": gas,
            "from": eth_account.address,
            "nonce": w3.eth.get_transaction_count(eth_account.address),
        }
    )
    return construct_txn, gas


if __name__ == "__main__":
    contract = get_precompile_contract()

    construct_txn, gas = create_contract_transaction(contract, *CONSTRUCTOR_ARGS)

    # Confirmation before deployment

    print(
        f"""
        CONTRACT DEPLOYMENT using {http_addr}

        Estimated Gas Usage   = {gas}
        Fee Per Gas           = {construct_txn['maxFeePerGas']}
        Estimated Total Cost  = {round(gas * construct_txn['maxFeePerGas'] / 1e18, 5)} ETH
        --------------------
    """
    )

    while True:
        response = input("Confirm? (Yes/No)")
        if response.lower() in ["yes", "y"]:
            signed_construct_txn = eth_account.sign_transaction(construct_txn)
            w3.eth.send_raw_transaction(signed_construct_txn.rawTransaction)
            break
        elif response.lower() in ["no", "n"]:
            print("Cancelling the transaction")
            break
        else:
            print("Please answer with Yes/No")
            continue
