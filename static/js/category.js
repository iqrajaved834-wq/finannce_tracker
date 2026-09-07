const addCategoryBtn = document.getElementById("addCategoryBtn");

if (addCategoryBtn) {
    addCategoryBtn.addEventListener("click", function () {
        window.location.href = "/add_category";
    });
}
const addCategoryForm = document.getElementById("addCategoryForm");

if (addCategoryForm) {

    addCategoryForm.addEventListener("submit", async function(event) {

        event.preventDefault();

        const name = document.getElementById("categoryName").value;
        const type = document.getElementById("categoryType").value;

        try {

            const response = await fetch("/categories", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    name: name,
                    type: type
                })
            });

            const data = await response.json();

            if (response.ok) {

                alert("✅ Category added successfully!");

                addCategoryForm.reset();

                window.location.href = "/categories-page";

            } else {

                alert(
                    "❌ " +
                    (data.error ||
                     data.Error ||
                     "Failed to add category.")
                );
            }

        } catch (error) {

            console.log("Something went wroong!!!!!") ;             

        }

    });
}

async function loadCategories() {

    const categoryContainer =
        document.getElementById("categorycontainer");

    if (!categoryContainer) {
        return;
    }

    try {

        const response = await fetch("/categories", {
            method: "GET"
        });

        const data = await response.json();

        if (response.ok) {

            const categories = data.Categories;

            categoryContainer.innerHTML = "";

            categories.forEach(function(category) {

                const categoryCard =
                    document.createElement("div");

                categoryCard.classList.add("category-card");

                categoryCard.innerHTML = `
                    <div class="category-icon">
                        ▦
                    </div>

                    <div class="category-info">

                        <strong>
                            ${category.name}
                        </strong>

                        <span>
                            ${category.type}
                        </span>

                    </div>
                `;

                categoryContainer.appendChild(categoryCard);

            });

        } else {

            categoryContainer.textContent =
                data.Error || "No categories found.";

        }

    } catch (error) {

        console.error("Error loading categories:", error);

        categoryContainer.textContent =
            "Failed to load categories.";

    }
}

loadCategories();