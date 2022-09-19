from pyteal import *
from pyteal.ast.bytes import Bytes
from pyteal_helpers import program


def approval():
    # globals
    global_owner = Bytes("owner")  # byteslice
    global_no_of_tokens_sold = Bytes("soldTokens")  # uint
    global_total_reward_claimed = Bytes("rewardClaimed")  # uint
    global_user_can_buy = Bytes("canBuy")  # uint
    global_user_can_claim = Bytes("canClaim")  # uint

    # Actions
    global_claim_reward = Bytes("claim")
    global_opt_in = Bytes("optIn")
    global_token_buy = Bytes("buyToken")
    global_contract_withdraw_tokens = Bytes("withdrawTokens")
    global_contract_withdraw_algos = Bytes("withdrawAlgos")
    global_toggle_onSale = Bytes("toggleBuy")
    global_toggle_can_claim = Bytes("toggleClaim")

    optIn = If(
        Txn.sender() == App.globalGet(global_owner),
        Seq(
            [
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields(
                    {
                        TxnField.type_enum: TxnType.AssetTransfer,
                        TxnField.asset_receiver: Global.current_application_address(),
                        TxnField.asset_amount: Int(0),
                        TxnField.xfer_asset: Txn.assets[
                            0
                        ],  # Must be in the assets array sent as part of the application call
                    }
                ),
                InnerTxnBuilder.Submit(),
                Approve(),
            ]
        ),
        Reject(),
    )

    # Buy tokens (Coins) from contract || MST Coin
    tokenBuy = Seq(
        program.check_self(
            group_size=Int(2),
            group_index=Int(0)
        ),
        program.check_rekey_zero(2),
        Assert(
            And(
                # check payment transaction
                Gtxn[1].type_enum() == TxnType.Payment,
                # check where is money going
                Gtxn[1].receiver() == Global.current_application_address(),
                # CloseRemainderTo or AssetCloseTo should be the intended recipient or equal to global ZeroAddress. An unchecked address could steal all the value!
                Gtxn[1].close_remainder_to() == Global.zero_address(),
                # check application arguments
                Txn.application_args.length() == Int(1),
                # checking token in on sale by the admin
                App.globalGet(global_user_can_buy) == Int(1),
            ),
        ),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields(
            {
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.asset_receiver: Txn.sender(),
                TxnField.asset_amount: (Gtxn[1].amount() / Int(10000)),
                TxnField.xfer_asset: Txn.assets[
                    0
                ],  # Must be in the assets array sent as part of the application call
            }
        ),
        InnerTxnBuilder.Submit(),
        App.globalPut(
            global_no_of_tokens_sold,
            App.globalGet(global_no_of_tokens_sold) + \
            (Gtxn[1].amount() / Int(10000))
        ),
        Approve(),
    )

    # owner call to pay someone their reward
    claimReward = If(
        And(
            Txn.sender() == App.globalGet(global_owner),
            App.globalGet(global_user_can_claim) == Int(1),
        ),
        Seq(
            [
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields(
                    {
                        TxnField.type_enum: TxnType.AssetTransfer,
                        TxnField.asset_receiver: Txn.accounts[1],
                        TxnField.asset_amount: Btoi(Txn.application_args[1]),
                        TxnField.xfer_asset: Txn.assets[
                            0
                        ],  # Must be in the assets array sent as part of the application call
                    }
                ),
                InnerTxnBuilder.Submit(),
                App.globalPut(
                    global_total_reward_claimed,
                    App.globalGet(global_total_reward_claimed) + \
                    Btoi(Txn.application_args[1])
                ),
                Approve(),
            ]
        ),
        Reject(),
    )

    # owner withdraw tokens coins
    withDrawTokens = If(
        Txn.sender() == App.globalGet(global_owner),
        Seq(
            [
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields(
                    {
                        TxnField.type_enum: TxnType.AssetTransfer,
                        TxnField.asset_receiver: Txn.sender(),
                        TxnField.asset_amount: Btoi(Txn.application_args[1]),
                        TxnField.xfer_asset: Txn.assets[
                            0
                        ],  # Must be in the assets array sent as part of the application call
                    }
                ),
                InnerTxnBuilder.Submit(),
                Approve(),
            ]
        ),
        Reject(),
    )

    withDrawAlgos = If(
        Txn.sender() == App.globalGet(global_owner),
        Seq(
            [
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields(
                    {
                        TxnField.type_enum: TxnType.Payment,
                        TxnField.amount: Btoi(Txn.application_args[1]),
                        TxnField.receiver: Txn.sender(),
                    }
                ),
                InnerTxnBuilder.Submit(),
                Approve(),
            ]
        ),
        Reject(),
    )

    # owner set sale on/off
    toggleOnSale = If(
        And(
            Txn.sender() == App.globalGet(global_owner),
            Btoi(Txn.application_args[1]) < Int(2)
        ),
        Seq(
            [
                App.globalPut(
                    global_user_can_buy,
                    Btoi(Txn.application_args[1])
                ),
                Approve(),
            ]
        ),
        Reject(),
    )

    # owner set claim on/off
    toggleOnClaim = If(
        And(
            Txn.sender() == App.globalGet(global_owner),
            Btoi(Txn.application_args[1]) < Int(2)
        ),
        Seq(
            [
                App.globalPut(
                    global_user_can_claim,
                    Btoi(Txn.application_args[1])
                ),
                Approve(),
            ]
        ),
        Reject(),
    )

    return program.event(
        init=Seq(
            [
                App.globalPut(global_owner, Txn.sender()),
                App.globalPut(global_user_can_claim, Int(0)),
                App.globalPut(global_user_can_buy, Int(0)),
                Approve(),
            ]
        ),
        no_op=Cond(
            [Txn.application_args[0] == global_token_buy, tokenBuy],
            [Txn.application_args[0] == global_opt_in, optIn],
            [Txn.application_args[0] == global_claim_reward, claimReward],
            [
                Txn.application_args[0] == global_contract_withdraw_tokens,
                withDrawTokens,
            ],
            [
                Txn.application_args[0] == global_contract_withdraw_algos,
                withDrawAlgos,
            ],
            [Txn.application_args[0] == global_toggle_onSale, toggleOnSale],
            [Txn.application_args[0] == global_toggle_can_claim, toggleOnClaim],
        ),
    )


def clear():
    return Approve()
