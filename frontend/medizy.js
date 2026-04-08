// ── NAVIGATION ──
function go(page){ window.location.href = page; }

// ── MOBILE MENU TOGGLE ──
function toggleMobileMenu(){
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const toggleBtn = document.querySelector('.mobile-menu-toggle');

    if(sidebar && overlay){
        sidebar.classList.toggle('open');
        overlay.classList.toggle('show');
    }
}

// ── RESPONSIVE HANDLING ──
function handleResponsive(){
    const toggleBtn = document.querySelector('.mobile-menu-toggle');
    const searchWrap = document.querySelector('.search-wrap');

    if(window.innerWidth <= 768){
        if(toggleBtn) toggleBtn.style.display = 'block';
        if(searchWrap) searchWrap.style.display = 'none';
    } else {
        if(toggleBtn) toggleBtn.style.display = 'none';
        if(searchWrap) searchWrap.style.display = 'block';
    }
}

// Initialize responsive handling
window.addEventListener('load', handleResponsive);
window.addEventListener('resize', handleResponsive);

// ── CLOCK ──
function startClock(clockId, dayId, dateId){
    function tick(){
        const now = new Date();
        if(document.getElementById(clockId))
            document.getElementById(clockId).textContent = now.toLocaleTimeString();
        if(document.getElementById(dayId))
            document.getElementById(dayId).textContent = now.toLocaleDateString(undefined,{weekday:'long'});
        if(document.getElementById(dateId))
            document.getElementById(dateId).textContent = now.toLocaleDateString();
    }
    setInterval(tick,1000); tick();
}

// ── MEDICINE LIST ──
const MEDICINES = [
    "Paracetamol","Crocin","Dolo 650","Vitamin C","ORS",
    "Ibuprofen","Cough Syrup","Zinc Tablets","Amoxicillin",
    "Vitamin D","Metformin","Aspirin","Ranitidine","Insulin",
    "Thyroxine","Diclofenac","Loratadine","Pantoprazole","Cetirizine"
];

// ── AUTOCOMPLETE (topbar & price search) ──
// inputId    : id of the <input>
// dropdownId : id of the .autocomplete-dropdown wrapper
// headerId   : id of the dropdown-header div
// listId     : id of the dropdown items container div
// targetPage : "search.html" (topbar) or "price-result.html" (price search)
// storageKey : localStorage key to save the query
function initAutocomplete(inputId, dropdownId, headerId, listId, targetPage, storageKey){
    const input    = document.getElementById(inputId);
    const dropdown = document.getElementById(dropdownId);
    const header   = document.getElementById(headerId);
    const list     = document.getElementById(listId);
    if(!input || !dropdown || !header || !list) return;

    let highlightIndex = -1;
    let currentMatches = [];

    function escapeRegex(str){ return str.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'); }

    function highlightMatch(name, query){
        const regex = new RegExp("("+escapeRegex(query)+")","gi");
        return name.replace(regex,"<mark>$1</mark>");
    }

    function openDropdown(matches, query){
        list.innerHTML = "";
        highlightIndex = -1;
        currentMatches = matches;
        if(matches.length === 0){
            header.textContent = "No results found";
            list.innerHTML = '<div class="dropdown-empty">😕 No medicine matched "<strong>'+query+'</strong>"</div>';
        } else {
            header.textContent = 'Results for "'+query+'"';
            matches.forEach(function(name){
                const item = document.createElement("div");
                item.className = "autocomplete-item";
                item.innerHTML = '<div class="item-icon">💊</div><span class="item-name">'+highlightMatch(name,query)+'</span><span class="item-tag">Medicine</span>';
                item.addEventListener("mousedown", function(e){ e.preventDefault(); selectItem(name); });
                list.appendChild(item);
            });
        }
        dropdown.classList.add("open");
    }

    function closeDropdown(){ dropdown.classList.remove("open"); highlightIndex = -1; }

    function selectItem(name){
        input.value = name;
        closeDropdown();
        localStorage.setItem(storageKey, name);
        window.location.href = targetPage + "?q=" + encodeURIComponent(name);
    }

    function updateHighlight(){
        list.querySelectorAll(".autocomplete-item").forEach(function(el,i){
            el.classList.toggle("highlighted", i === highlightIndex);
        });
    }

    input.setAttribute("autocomplete","off");

    input.addEventListener("input", function(){
        const query = input.value.trim();
        if(!query){ closeDropdown(); return; }
        const matches = MEDICINES.filter(function(m){ return m.toLowerCase().includes(query.toLowerCase()); });
        openDropdown(matches, query);
    });

    input.addEventListener("keydown", function(e){
        const items = list.querySelectorAll(".autocomplete-item");
        if(e.key === "ArrowDown"){ e.preventDefault(); highlightIndex = Math.min(highlightIndex+1, items.length-1); updateHighlight(); items[highlightIndex]&&items[highlightIndex].scrollIntoView({block:"nearest"}); }
        else if(e.key === "ArrowUp"){ e.preventDefault(); highlightIndex = Math.max(highlightIndex-1,-1); updateHighlight(); if(highlightIndex>=0) items[highlightIndex]&&items[highlightIndex].scrollIntoView({block:"nearest"}); }
        else if(e.key === "Enter"){
            if(highlightIndex>=0 && currentMatches[highlightIndex]){ e.preventDefault(); selectItem(currentMatches[highlightIndex]); }
            else { const q=input.value.trim(); if(q){ closeDropdown(); localStorage.setItem(storageKey,q); window.location.href=targetPage+"?q="+encodeURIComponent(q); } }
        }
        else if(e.key === "Escape"){ closeDropdown(); }
    });

    document.addEventListener("click", function(e){
        if(!input.contains(e.target) && !dropdown.contains(e.target)) closeDropdown();
    });
}

// ── SEARCH (topbar — legacy, kept for compatibility) ──
function initSearch(inputId){
    // Now delegates to initAutocomplete using standard topbar IDs
    initAutocomplete(inputId, "autocompleteDropdown", "dropdownHeader", "dropdownList", "search.html", "searchQuery");
}

// ── TOAST ──
function showToast(msg, color){
    const t = document.getElementById("toast");
    if(!t) return;
    t.textContent = msg;
    t.style.background = color||"#EF4444";
    t.style.display = "block";
    setTimeout(()=>{ t.style.display="none"; }, 3500);
}
