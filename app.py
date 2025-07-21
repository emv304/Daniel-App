import streamlit as st
import requests
import os
import urllib.parse

APP_VERSION = "1.0.58"  # Daniel App - 2025-07-20

st.set_page_config(page_title="Daniel Model/Serial Finder", layout="centered")
st.title("Daniel: Get Model & Serial Number From a Picture")
st.caption(f"App Version: {APP_VERSION}")

def get_date_of_manufacture(model, serial):
    manufacturer = detect_manufacturer(model)
    if manufacturer == "GE":
        return ge_date_of_manufacture(serial)
    elif manufacturer == "Whirlpool":
        return whirlpool_date_of_manufacture(serial)
    elif manufacturer == "Frigidaire":
        return frigidaire_date_of_manufacture(serial)
    elif manufacturer == "LG":
        return lg_date_of_manufacture(serial)
    elif manufacturer == "Samsung":
        return samsung_date_of_manufacture(serial)
    elif manufacturer == "Maytag":
        return maytag_date_of_manufacture(serial)
    elif manufacturer == "Bosch/Gaggenau/Siemens/Thermador":
        return bosch_date_of_manufacture(serial)
    elif manufacturer == "Miele":
        return "Date of manufacture for Miele appliances cannot be determined from the serial number alone. Please contact Miele support."
    elif manufacturer == "Wolf/SubZero/Cove":
        return wolf_subzero_cove_date_of_manufacture(serial)
    else:
        return "Could not determine manufacture date: unknown manufacturer"

def detect_manufacturer(model):
    model = (model or "").upper()
    if model.startswith(("J", "JB", "JG", "JS", "G", "Z", "P", "D", "C")):
        return "GE"
    if model.startswith(("W", "Y", "R")):
        return "Whirlpool"
    if model.startswith(("F", "E", "P")):
        return "Frigidaire"
    if model.startswith(("L", "WM", "DLE")):
        return "LG"
    if model.startswith(("S", "WA", "RF")):
        return "Samsung"
    if model.startswith(("M", "MDB", "MHW")):
        return "Maytag"
    if model.startswith(("SH", "WAT", "WT", "T", "G", "HB", "SN", "WM", "HS")):
        return "Bosch/Gaggenau/Siemens/Thermador"
    miele_prefixes = ("W", "G", "KM", "H", "T", "D", "F", "S")
    if any(model.startswith(pref) for pref in miele_prefixes) and len(model) > 2:
        return "Miele"
    if model.startswith(("S", "Z", "C")):
        return "Wolf/SubZero/Cove"
    return "Unknown"

def ge_date_of_manufacture(serial):
    if not serial or len(serial.strip()) < 2:
        return "Could not determine manufacture date from serial number"
    serial = serial.strip().upper()
    months = {
        "A": "January", "D": "February", "F": "March", "G": "April",
        "H": "May", "L": "June", "M": "July", "R": "August",
        "S": "September", "T": "October", "V": "November", "Z": "December"
    }
    years = {
        "A": 2013, "D": 2014, "F": 2015, "G": 2016,
        "H": 2017, "L": 2018, "M": 2019, "R": 2020,
        "S": 2021, "T": 2022, "V": 2023, "Z": 2024
    }
    month_letter = serial[0]
    year_letter = serial[1]
    month = months.get(month_letter)
    year = years.get(year_letter)
    if month and year:
        return f"{month} {year}"
    elif not month and year:
        return f"Unknown month code {month_letter}, {year}"
    elif month and not year:
        return f"{month}, unknown year code {year_letter}"
    else:
        return "Could not determine manufacture date from serial number"

def whirlpool_date_of_manufacture(serial):
    if serial and len(serial) >= 3:
        year_code = serial[1].upper()
        month_code = serial[2].upper()
        year_table = {
            'Y': 2009, 'Z': 2010, 'A': 2011, 'B': 2012, 'C': 2013, 'D': 2014,
            'E': 2015, 'F': 2016, 'G': 2017, 'H': 2018, 'J': 2019, 'K': 2020,
            'L': 2021, 'M': 2022, 'N': 2023, 'P': 2024, 'R': 2025, 'S': 2016,
            'T': 2017, 'V': 2018, 'W': 2019, 'X': 2020,
        }
        month_table = {
            'A': 'January', 'B': 'February', 'C': 'March', 'D': 'April',
            'E': 'May', 'F': 'June', 'G': 'July', 'H': 'August',
            'J': 'September', 'K': 'October', 'L': 'November', 'M': 'December'
        }
        year = year_table.get(year_code)
        month = month_table.get(month_code)
        if year and month:
            return f"{month} {year}"
    if serial and len(serial) >= 6:
        year_str = serial[2:4]
        week_str = serial[4:6]
        if year_str.isdigit() and week_str.isdigit():
            year = int(year_str)
            week = int(week_str)
            if year >= 90:
                year += 1900
            else:
                year += 2000
            return f"Week {week} of {year}"
    return "Could not determine manufacture date from serial number"

def frigidaire_date_of_manufacture(serial):
    if serial and len(serial) >= 4:
        year_str = serial[0:2]
        week_str = serial[2:4]
        if year_str.isdigit() and week_str.isdigit():
            year = int(year_str)
            week = int(week_str)
            year += 2000 if year < 50 else 1900
            return f"Week {week} of {year}"
    return "Could not determine manufacture date from serial number"

def lg_date_of_manufacture(serial):
    if serial and len(serial) >= 3:
        year_str = serial[0]
        month_str = serial[1:3]
        if year_str.isdigit() and month_str.isdigit():
            year_digit = int(year_str)
            month = int(month_str)
            year = 2010 + year_digit
            return f"{month:02d}/{year}"
    return "Could not determine manufacture date from serial number"

def samsung_date_of_manufacture(serial):
    year_codes = "ABCDEFGHJKLMNPQRSTUWXYZ"
    month_codes = "123456789ABC"
    if serial and len(serial) >= 2:
        year_char = serial[0].upper()
        month_char = serial[1].upper()
        if year_char in year_codes and month_char in month_codes:
            year_index = year_codes.index(year_char)
            year = 1997 + year_index
            month_index = month_codes.index(month_char)
            month = month_index + 1
            return f"{month:02d}/{year}"
    return "Could not determine manufacture date from serial number"

def maytag_date_of_manufacture(serial):
    return whirlpool_date_of_manufacture(serial)

def bosch_date_of_manufacture(serial):
    if serial and len(serial) >= 4:
        week_str = serial[0:2]
        year_str = serial[2:4]
        if week_str.isdigit() and year_str.isdigit():
            week = int(week_str)
            year = int(year_str) + 2000
            return f"Week {week} of {year}"
    return "Could not determine manufacture date from serial number"

def wolf_subzero_cove_date_of_manufacture(serial):
    if serial and len(serial) >= 4 and serial[:4].isdigit():
        year = 2000 + int(serial[:2])
        week = int(serial[2:4])
        return f"Week {week} of {year}"
    return "Could not determine manufacture date from serial number"

# ---- Main App ----

option = st.radio(
    "How would you like to provide the image or info?",
    ["Upload a photo", "Take a photo", "Enter manually"]
)

model = None
serial = None
image_data = None
image_filename = "image.jpg"

if option == "Upload a photo":
    uploaded_image = st.file_uploader("Upload an image (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        image_data = uploaded_image.getvalue()
        image_filename = uploaded_image.name
        st.image(uploaded_image, caption="Your uploaded image", width=400)
elif option == "Take a photo":
    captured_image = st.camera_input("Take a photo")
    if captured_image is not None:
        image_data = captured_image.getvalue()
        image_filename = "image.png"
        st.image(captured_image, caption="Your captured photo", width=400)
elif option == "Enter manually":
    st.info("Enter the model and serial number below.")
    model = st.text_input("Model Number")
    serial = st.text_input("Serial Number")

if (
    (image_data is not None) or
    (option == "Enter manually" and model and serial)
):
    if option == "Enter manually":
        detected_model = model
        detected_serial = serial
    else:
        _, ext = os.path.splitext(image_filename.lower())
        image_type = "image/png" if ext == ".png" else "image/jpeg"
        files = {"image": (image_filename, image_data, image_type)}
        url = "https://www.ontrack.tools/api/scan-appliance"
        with st.spinner("Getting model and serial number..."):
            response = requests.post(url, files=files)
            try:
                data = response.json()
                detected_model = data.get("modelNumber") or data.get("model")
                detected_serial = data.get("serialNumber") or data.get("serial")
            except Exception as e:
                st.error("Could not read the model or serial from the server's response.")
                detected_model = None
                detected_serial = None

    manufacturer = detect_manufacturer(detected_model)
    st.markdown(f"**Detected Manufacturer:** {manufacturer}")

    st.markdown("#### Model & Serial Number")
    cols = st.columns([2, 2])
    with cols[0]:
        st.write("**Model:**")
        st.text_input(
            label="Model (copy manually)",
            value=detected_model or "",
            key="copy_model",
            label_visibility="collapsed"
        )
    with cols[1]:
        st.write("**Serial:**")
        st.text_input(
            label="Serial (copy manually)",
            value=detected_serial or "",
            key="copy_serial",
            label_visibility="collapsed"
        )
    st.caption("Click in a field, then press Ctrl+C (or ⌘+C) to copy.")

    date_info = get_date_of_manufacture(detected_model, detected_serial)
    if "Could not" in date_info or "cannot be determined" in date_info.lower():
        st.error(date_info)
    else:
        st.info(f"Date of Manufacture: {date_info}")

    # --------- Button links with checkmarks ----------
    if detected_model:
        st.markdown("### Parts and Manuals")
        encoded_model = urllib.parse.quote(detected_model)
        all_links = [
            ("Appliance Parts Pros", f"https://www.appliancepartspros.com/search.aspx?model={encoded_model}"),
            ("Appliantology", f"https://appliantology.org/search/?q={encoded_model}"),
            ("Bosch", f"https://www.bosch-home.com/us/supportdetail/product/{encoded_model}"),
            ("Encompass Parts", f"https://encompass.com/modelsearch_results.aspx?searchTerm={encoded_model}"),
            ("ManualsLib", f"https://www.manualslib.com/search.html?q={encoded_model}"),
            ("Marcone", f"https://www.marcone.com/marcone-sso/login.jsp?modelNumber={encoded_model}"),
            ("PartsDr", f"https://partsdr.com/search/search.php?q={encoded_model}"),
            ("PartSelect", f"https://www.partselect.com/ModelSearch.aspx?ModelNum={encoded_model}"),
            ("Repair Clinic", f"https://www.repairclinic.com/Shop-For-Parts?modelNumber={encoded_model}"),
            ("Reliable Parts", f"https://www.reliableparts.com/search?q={encoded_model}"),
            ("Sears PartsDirect", f"https://www.searspartsdirect.com/model-search.html?q={encoded_model}"),
            ("Tribles", f"https://www.tribles.com/search?q={encoded_model}"),
            ("V&V Appliance Parts", f"https://www.vvapplianceparts.com/ModelSearch.aspx?ModelNumber={encoded_model}"),
        ]

        if "visited_links" not in st.session_state or len(st.session_state["visited_links"]) != len(all_links):
            st.session_state["visited_links"] = [False] * len(all_links)

        st.write("Click a button to open a site. ✔️ = clicked in this session.")

        for idx, (label, url) in enumerate(all_links):
            cols = st.columns([0.1, 0.8, 0.1])
            with cols[0]:
                if st.session_state["visited_links"][idx]:
                    st.write("✔️")
                else:
                    st.write("")
            with cols[1]:
                btn = st.button(label, key=f"btn_{idx}")
                if btn:
                    st.session_state["visited_links"][idx] = True
                    js = f"window.open('{url}', '_blank')"
                    st.components.v1.html(f"<script>{js}</script>", height=0)
                    st.rerun()   # <---- Fixed here!
            with cols[2]:
                pass

else:
    if option != "Enter manually":
        st.info("Please upload or take a photo of an appliance label.")
