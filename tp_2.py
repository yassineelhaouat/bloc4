import algokit_utils as au
import algosdk as sdk
from algokit_utils import AlgoAmount
from algokit_utils.transactions import AppCallMethodCallParams, PaymentParams
from utils import (
    account_creation,
    display_info,
)

algorand = au.AlgorandClient.from_environment()


algod_client = algorand.client.algod
indexer_client = algorand.client.indexer    

print(algod_client.block_info(0))
print(indexer_client.health())
alice = account_creation(algorand, "ALICE", au.AlgoAmount(algo=10_000))
bob = account_creation(algorand, "BOB", au.AlgoAmount(algo=100))
display_info(algorand, ["ALICE", "BOB"])


token = algorand.send.asset_create(
    au.AssetCreateParams(
        sender=alice.address,
        total=15,
        decimals=0,
        default_frozen=False,
        unit_name="TST",
        asset_name="Alice asset",
    )
)
print(token.asset_id)


#####

result = (
    algorand.new_group()
    .add_asset_opt_in(
        au.AssetOptInParams(
            sender=bob.address,
            asset_id=token.asset_id,
            signer=bob.signer,
        ))
        
    .add_payment(PaymentParams(
        sender=bob.address,
        receiver=alice.address,
        amount=AlgoAmount.from_algo(1),
    ))
    .add_asset_transfer(
        au.AssetTransferParams(
            sender=alice.address,
            receiver=bob.address,
            amount=1,
            asset_id=token.asset_id,
        ))
    .send()
)


print(result.confirmations)

