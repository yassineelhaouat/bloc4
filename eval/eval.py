import os
if not os.path.exists("client.py"):
    os.system("algokit compile py --out-dir ./app app.py")
    os.system("algokit generate client app/Eval.arc32.json --output client.py")


import algokit_utils as au
import algokit_utils.transactions.transaction_composer as att


algorand = au.AlgorandClient.testnet()

with open(".env", "r") as file:
    mnemonic = file.read()
yass = algorand.account.from_mnemonic(mnemonic=mnemonic)
import client as cl
eval_factory = cl.EvalFactory(
    algorand=algorand,
    default_sender=yass.address
    )
app_id = 736038676
eval_client = eval_factory.get_app_client_by_id(app_id)

print(f"Account address: {yass.address}")

###################Q1###################
try:
    result = eval_client.send.claim_algo(
        params=au.CommonAppCallParams(
            sender=yass.address,
            signer=yass.signer,
            box_references=[yass.public_key, b"q1" + yass.public_key]
        )
    )
    print(f"Claimed Algo: {result}")
except Exception as e:
    print(f"Error claiming Algo")

###################Q2###################
try:
    res_asset = algorand.send.asset_create(
        au.AssetCreateParams(
            sender=yass.address,
            signer=yass.signer,
            total=15,
            decimals=0,
            default_frozen=False,
            unit_name="PY-CL-FD",  # 8 Max
            asset_name="Proof of Attendance Py-Clermont",
            url="https://pyclermont.org/",
            note="Hello Clermont",
        )
    )
    asset_id = res_asset.confirmation["asset-index"]
    print(f"Created asset with ID: {asset_id}")
except Exception as e:
    print(f"Error creating asset")
    asset_id = None

# Only proceed with opt-in if asset was created

sp = algorand.get_suggested_params()
mbr_pay_txn = algorand.create_transaction.payment(
    au.PaymentParams(
        sender=yass.address,
        receiver=eval_client.app_address,
        amount=au.AlgoAmount(algo=0.2),
        extra_fee=au.AlgoAmount(micro_algo=sp.min_fee)
    )
)
try:
    result = eval_client.send.opt_in_to_asset(
        cl.OptInToAssetArgs(
            asset=asset_id,
            mbr_pay=att.TransactionWithSigner(mbr_pay_txn, yass.signer),
        ),
        send_params=au.SendParams(populate_app_call_resources=True)
    )
    print(f"Opted in to ASA: {result}")
except Exception as e:
    print(f"Error opting in to ASA")

###################Q3###################
try:
    array = bytes([5, 6])
    result = eval_client.send.sum(
        cl.SumArgs(
            array=array
        ),
        params=au.CommonAppCallParams(
            sender=yass.address,
            signer=yass.signer,
            box_references=[yass.public_key, b"q3" + yass.public_key]
        )
    )
    print(f"Sum: {result}")
except Exception as e:
    print(f"Error summing")

###################Q4###################
try:
    box_value = algorand.app.get_box_value(app_id, box_name=yass.public_key)
    print(f"Current box value: {box_value}")
except Exception as e:
    print(f"Error getting box value")

try:
    result = eval_client.send.update_box(
        cl.UpdateBoxArgs(
            value="YASS"
        ),
        params=au.CommonAppCallParams(
            sender=yass.address,
            signer=yass.signer,
            box_references=[yass.public_key, b"q4" + yass.public_key]
        )
    )
    print(f"Updated box: {result}")
    
    try:
        box_value = algorand.app.get_box_value(app_id, box_name=yass.public_key)
        print(f"New box value: {box_value}")
    except Exception as e:
        print(f"Error getting updated box value")
except Exception as e:
    print(f"Error updating box")

