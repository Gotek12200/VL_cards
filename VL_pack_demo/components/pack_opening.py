import streamlit as st
import streamlit.components.v1 as components
import time
import random

from utils.media import img_data_uri, play_sound


def flash_screen():
    st.markdown(
        """
        <style>
        @keyframes flash {
            0% {background-color: white;}
            100% {background-color: transparent;}
        }
        .flash {
            position: fixed;
            top:0; left:0;
            width:100vw; height:100vh;
            animation: flash 0.6s ease-out;
            pointer-events:none;
            z-index:9999;
        }
        </style>
        <div class="flash"></div>
        """,
        unsafe_allow_html=True
    )

def show_shaking_pack(container, pack_rel_path: str = "assets/packs/pack.png", width_px: int = 250):
    pack_src = img_data_uri(pack_rel_path)
    container.markdown(
        f"""
        <style>
        @keyframes shake {{
          0% {{ transform: translate(1px, 1px) rotate(0deg); }}
          25% {{ transform: translate(-3px, 0px) rotate(-1deg); }}
          50% {{ transform: translate(3px, 2px) rotate(1deg); }}
          75% {{ transform: translate(-1px, 2px) rotate(1deg); }}
          100% {{ transform: translate(1px, -2px) rotate(-1deg); }}
        }}
        .pack {{
            animation: shake 0.6s infinite;
            width:{width_px}px;
            display:block;
            margin:auto;
        }}
        </style>
        <img class="pack" src="{pack_src}">
        """,
        unsafe_allow_html=True
    )


def generate_fake_pack():
    rarities = ["Common", "Common", "Rare", "Epic", "Legendary"]
    random.shuffle(rarities)

    cards = []
    for i, rarity in enumerate(rarities):
        cards.append({
            "image": f"assets/cards/c{i+1}.png",
            "rarity": rarity
        })
    return cards

def reveal_cards(cards):
    rarity_colors = {
        "Common": "#bbbbbb",
        "Rare": "#4da6ff",
        "Epic": "#b84dff",
        "Legendary": "#ffcc00"
    }

    cols = st.columns(len(cards))
    placeholders = [col.empty() for col in cols]

    for i, card in enumerate(cards):
        time.sleep(0.9)

        play_sound("assets/sfx/card_flip.mp3")
        if card["rarity"] == "Epic":
            play_sound("assets/sfx/epic.mp3")
        if card["rarity"] == "Legendary":
            play_sound("assets/sfx/legendary.mp3")

        color = rarity_colors.get(card["rarity"], "#ffffff")
        card_src = img_data_uri(card["image"])

        placeholders[i].markdown(
    f"""
    <style>
    .card-hover {{
        transition: transform 0.25s ease, filter 0.25s ease;
    }}
    .card-hover:hover {{
        transform: scale(1.18);
        filter:
          drop-shadow(0 0 35px {color})
          drop-shadow(0 0 70px {color});
        z-index: 999;
    }}
    </style>

    <div style="text-align:center; animation: pop 0.4s ease-out;">
        <img class="card-hover" src="{card_src}" width="190"
             style="
                filter:
                  drop-shadow(0 0 25px {color})
                  drop-shadow(0 0 50px {color});
             ">
        <div style="margin-top:6px; color:{color}; font-weight:700;">
            {card["rarity"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


def run_pack_open_sequence():
    play_sound("assets/sfx/pack_open.mp3")
    flash_screen()

    # Pack placeholder (we will clear it)
    pack_slot = st.empty()
    show_shaking_pack(pack_slot, "assets/packs/pack.png", width_px=260)

    time.sleep(3)

    # Remove pack before revealing cards
    pack_slot.empty()

    # Reveal cards
    cards = generate_fake_pack()
    reveal_cards(cards)

