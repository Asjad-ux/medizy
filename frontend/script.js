// =======================
// 🔹 SEND OTP
// =======================
async function sendOTP(email) {
  const res = await fetch("http://localhost:3000/api/send-otp", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email })
  });

  return await res.json();
}


// =======================
// 🔹 SIGNUP
// =======================
async function handleSignup() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const phone = document.getElementById("phone").value;

  // 🔥 temporary store for OTP page
  localStorage.setItem("userEmail", email);
  localStorage.setItem("userPassword", password);
  localStorage.setItem("userPhone", phone);

  const data = await sendOTP(email);

  if (data.success) {
    alert("OTP Sent ✅");
    window.location.href = "otp.html";
  } else {
    alert("Error sending OTP ❌");
  }
}


// =======================
// 🔹 LOGIN
// =======================
async function handleLogin() {

  console.log("LOGIN CLICKED 🔥");

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const res = await fetch("http://localhost:3000/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    console.log("RESPONSE:", data);

    if (data.success) {

      // 🔥 SAVE DATA (MOST IMPORTANT)
      localStorage.setItem("userEmail", data.user.email);
      localStorage.setItem("userPassword", data.user.password);
      localStorage.setItem("userPhone", data.user.phone);

      console.log("DATA SAVED IN LOCALSTORAGE ✅");

      window.location.href = "dashboard.html";

    } else {
      showToast("Invalid Credentials ❌");
    }

  } catch (error) {
    console.log("ERROR:", error);
    showToast("Server not running ❌");
  }
}


// =======================
// 🔹 TOAST MESSAGE
// =======================
function showToast(message) {
  const toast = document.getElementById("toast");

  if (!toast) return;

  toast.innerText = message;
  toast.style.display = "block";

  setTimeout(() => {
    toast.style.display = "none";
  }, 3000);
}
function getDirection(lat, lng){

    // Default location (Delhi)
    const userLat = 28.500728498757884;
    const userLng = 77.2913550643292;

    // Google Maps URL
    const url = `https://www.google.com/maps/dir/?api=1&origin=${userLat},${userLng}&destination=${lat},${lng}`;

    // Open in new tab
    window.open(url, "_blank");
}

async function registerPharmacy() {
    console.log("Button clicked");
    const name = document.getElementById("name").value;
    const address = document.getElementById("address").value;
    const gst = document.getElementById("gst").value;

    if (!name || !address || !gst) {
        alert("Please fill all fields");
        return;
    }

    try {
        const res = await fetch("http://localhost:3000/api/register-pharmacy", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name, address, gst })
        });

        const data = await res.json();

        if (data.success) {
            alert("Pharmacy Registered Successfully!");
            window.location.href = "pharmacy-upload.html"; // redirect
        } else {
            alert("Error saving data");
        }

    } catch (err) {
        console.log(err);
        alert("Server error");
    }
}