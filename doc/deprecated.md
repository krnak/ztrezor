Functionalities:

| Name                    | Input                                      | Output                           |  
|-------------------------|--------------------------------------------|----------------------------------|    
| ZIP32 keygen            | `secret`, `i`                              | `sk`                             |  
| Key components gen      | `sk`                                       | `ask`, `fvk`, `ivk`, `ovk`, `dk` |  
| Address diversifier     | `dk`, `ivk`, `index`                       | `addr`                           |  
| Action shielder         | `action_plain`, `rseed`,`aplha`,`rcv`      | `action_shielded`                |  
| Note decryption via ivk | `ivk`, `epk`, `C_enc`                      | `note_plain` or failture         |  
| Note decryption via ovk | `ovk`, `epk`, `C_out`, `C_enc`, `cm`, `cv` | `note_plain`                     |
| Nullifier gen           | `nk`, `rseed`, `cm`, `nf_old`              | `nf_new`                         |  
| Spend signer            | `SIGHASH`, `ask`, `alpha`                  | `spendAuthSig`                   |  
| Binding signer          | `SIGHASH`, `rcv[]`, `cv_net`               | `bindingSig`                     |  
| Prover                  | `action_plain[]`, `action_shielded[]`, `fvk`, `alpha[]`, `rcv[]`, `rssed[]`, `cv_net`  | `proof` |

If the `nf` was not computed in the Trezor, its integrity cannot be checked. Therefore user cannot control which of his Notes was spent. But since `cv` and `cm` were computed in the Trezor, user controls the value of the input Note of an Action. If a nullifier of a Note with a different value was sent by the Host, then the zk-proof must be invalid. (`cm` binds the Action to output `v_new` ZEC and `cv` binds the Action to add exactly `v_old - v_new` ZEC to a shielded transaction pool. Though `cm` and `cv` together bind the Action to has `c_old` ZEC on input). To sum it up, once the `cv` and `cm` were computed in the Trezor, then the only new freedom of the Host, who controls the nullifier, is to choose, which of user's Notes with value exactly `v_old` ZEC is spent as an Action input. Since the transaction inputs were selected by the Host anyway, the Host has this freedom anyway.