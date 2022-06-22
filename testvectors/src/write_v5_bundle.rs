/// Functions for parsing & serialization of Orchard transaction components.
use std::convert::TryFrom;
use std::io::{self, Read, Write};

//use nonempty::NonEmpty;
use orchard::{
    builder::{InProgress, SigningMetadata, Unauthorized, Unproven},
    bundle::{Authorization, Authorized, Flags},
    note::{ExtractedNoteCommitment, Nullifier, TransmittedNoteCiphertext},
    primitives::redpallas::{self, SigType, Signature, SpendAuth, VerificationKey},
    value::ValueCommitment,
    Action, Anchor,
};
//use zcash_encoding::{Array, CompactSize, Vector};

/// Writes an [`orchard::Bundle`] in the v5 transaction format.
pub fn write_v5_bundle<W: Write>(
    bundle: Option<&orchard::Bundle<InProgress<Unproven, Unauthorized>, i64>>,
    mut writer: W,
) -> io::Result<()> {
    if let Some(bundle) = &bundle {
        //writer.write_all(&[bundle.actions().len() as u8][..])?;
        for act in bundle.actions().iter() {
            write_action_without_auth(&mut writer, act)?;
        }
        writer.write_all(&[bundle.flags().to_byte()])?;
        writer.write_all(&bundle.value_balance().to_le_bytes())?;
        writer.write_all(&bundle.anchor().to_bytes())?;
    } else {
    }

    Ok(())
}

pub fn write_value_commitment<W: Write>(mut writer: W, cv: &ValueCommitment) -> io::Result<()> {
    writer.write_all(&cv.to_bytes())
}

pub fn write_nullifier<W: Write>(mut writer: W, nf: &Nullifier) -> io::Result<()> {
    writer.write_all(&nf.to_bytes())
}

pub fn write_verification_key<W: Write>(
    mut writer: W,
    rk: &redpallas::VerificationKey<SpendAuth>,
) -> io::Result<()> {
    writer.write_all(&<[u8; 32]>::from(rk))
}

pub fn write_cmx<W: Write>(mut writer: W, cmx: &ExtractedNoteCommitment) -> io::Result<()> {
    writer.write_all(&cmx.to_bytes())
}

pub fn write_note_ciphertext<W: Write>(
    mut writer: W,
    nc: &TransmittedNoteCiphertext,
) -> io::Result<()> {
    writer.write_all(&nc.epk_bytes)?;
    writer.write_all(&nc.enc_ciphertext)?;
    writer.write_all(&nc.out_ciphertext)
}

pub fn write_action_without_auth<W: Write>(
    mut writer: W,
    act: &Action<SigningMetadata>,
) -> io::Result<()> {
    write_value_commitment(&mut writer, act.cv_net())?;
    write_nullifier(&mut writer, act.nullifier())?;
    write_verification_key(&mut writer, act.rk())?;
    write_cmx(&mut writer, act.cmx())?;
    write_note_ciphertext(&mut writer, act.encrypted_note())?;
    Ok(())
}
