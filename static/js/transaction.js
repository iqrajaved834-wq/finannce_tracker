const addTransactionPageBtn =
    document.getElementById("addTransactionPageBtn");

if (addTransactionPageBtn) {
    addTransactionPageBtn.addEventListener("click", function () {
        window.location.href = "/add-transaction";
    });
}


const addTransactionForm =
    document.getElementById("addTransactionForm");

if (addTransactionForm) {

    addTransactionForm.addEventListener("submit", async function(event) {

        event.preventDefault();
        const description =
            document.getElementById("addTransactionDescription").value;

        const amount =
            document.getElementById("addTransactionAmount").value;

        const category_id =
            document.getElementById("addTransactionCategory").value;

        const type =
            document.getElementById("addTransactionType").value;

        const transaction_date =
            document.getElementById("addTransactionDate").value;
        const message =
            document.getElementById("addTransactionMessage");



        const transactionData = {

            description: description,
            amount: amount,
            category_id: category_id,
            type: type,
            transaction_date: transaction_date

        };


        try {

            const response = await fetch("/transactions", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(transactionData)

            });


            const data = await response.json();
           if (response.ok) {

           alert("✅ Transaction added successfully!");

           addTransactionForm.reset();
        } else {

        alert(
        "❌ " +
        (data.error || data.Error || "Failed to add transaction.")
        );

}

        } catch (error) {

            console.log(error);

            message.textContent =
                "Something went wrong. Please try again.";

        }

    });
}

async function loadCategoriesForAddTransaction() {
    const categoryDropdown =
        document.getElementById("addTransactionCategory");
    if (!categoryDropdown) {
        return;
    }

    try {

        const response = await fetch("/categories", {
            method: "GET"
        });
        const data = await response.json();
        if (!response.ok) {

            console.log(
                data.error || data.Error
            );

            return;
        }


        const categories = data.Categories;
        categoryDropdown.innerHTML =
            '<option value="">Select Category</option>';
        categories.forEach(function(category) {
            const option =
                document.createElement("option");
            option.value =
                category.category_id;
            option.textContent =
                category.name;
            categoryDropdown.appendChild(option);

        });

    } catch (error) {

        console.log(
            "Something went wrong while loading categories.",
            error
        );

    }
}
loadCategoriesForAddTransaction();


async function loadCategoriesForTransactionFilter() {
    const categoryDropdown =
        document.getElementById("transactionCategoryFilter");
    if (!categoryDropdown) {
        return;
    }

    try {

        const response = await fetch("/categories", {
            method: "GET"
        });

        const data = await response.json();
        if (!response.ok) {

            console.log(
                data.error || data.Error
            );

            return;
        }

        const categories = data.Categories;
        categoryDropdown.innerHTML =
            '<option value="">All Categories</option>';

        categories.forEach(function(category) {

            const option =
                document.createElement("option");
            option.value =
                category.category_id;
            option.textContent =
                category.name;
            categoryDropdown.appendChild(option);

        });

    } catch (error) {

        console.log(
            "Something went wrong while loading categories.",
            error
        );

    }
}
loadCategoriesForTransactionFilter();


async function loadTransactionTable() {

    const category =
        document.getElementById("transactionCategoryFilter").value;

    const month =
        document.getElementById("transactionMonthFilter").value;

    const tableBody =
        document.getElementById("transactionsPageTableBody");


    const params = new URLSearchParams();

    if (category) {
        params.append("category_id", category);
    }

    if (month) {
        params.append("month", month);
    }


    let url = "/transactions";

    if (params.toString()) {
        url += "?" + params.toString();
    }


    try {

        const response = await fetch(url, {
            method: "GET"
        });

        const data = await response.json();

        if (!response.ok) {
            console.log(data.error || data.Error);
            return;
        }


        const transactions = data.Transaction;
         const categoryResponse =
            await fetch("/categories");

        const categoryData =
            await categoryResponse.json();

        const categories =
            categoryData.Categories;


        const categoryMap = {};

        categories.forEach(function(category) {

            categoryMap[category.category_id] =
                category.name;

        });


        tableBody.innerHTML = "";
        if (transactions.length === 0) {

            tableBody.innerHTML = `
                <tr>
                    <td colspan="6" class="transactions-empty">
                        No transactions found.
                    </td>
                </tr>
            `;

            return;
        }
        transactions.forEach(function(transaction) {

            const row =
                document.createElement("tr");


            const categoryName =
                categoryMap[transaction.category_id]
                || "Unknown Category";


            const amountClass =
                transaction.type === "income"
                ? "transaction-income-amount"
                : "transaction-expense-amount";


            const badgeClass =
                transaction.type === "income"
                ? "transaction-income-badge"
                : "transaction-expense-badge";


            const amountSign =
                transaction.type === "income"
                ? "+"
                : "-";


            row.innerHTML = `

                <td>${transaction.transaction_date}</td>

                <td>${transaction.description}</td>

                <td>${categoryName}</td>

                <td>
                    <span class="${badgeClass}">
                        ${transaction.type}
                    </span>
                </td>

                <td class="${amountClass}">
                    ${amountSign} Rs.
                    ${Number(transaction.amount).toLocaleString()}
                </td>

                <td>

                    <div class="transaction-actions">

                        <button
                            type="button"
                            class="transaction-edit-action"
                            onclick="window.location.href='/edit-transaction/${transaction.transaction_id}'"
                        >
                            <span>✎</span>
                        </button>

                        <button
                            type="button"
                            class="transaction-delete-action"
                            onclick="deleteTransaction(${transaction.transaction_id})"
                        >
                            <span>🗑</span>
                        </button>

                    </div>

                </td>
            `;


            tableBody.appendChild(row);

        });


    } catch (error) {

        console.log("FILTER ERROR:", error);

    }
}


const transactionFilterBtn =
    document.getElementById("transactionFilterBtn");

if (transactionFilterBtn) {

    transactionFilterBtn.addEventListener(
        "click",
        function() {

            loadTransactionTable();

        }
    );
}

async function deleteTransaction(transaction_id) {

    try {
        const response = await fetch(
            `/transactions/${transaction_id}`,
            {
                method: "DELETE"
            }
        );
        const data = await response.json();
       
       if (response.ok) {

       alert("✅ Transaction deleted successfully!");

       loadTransactionTable();

        } else {

        alert(
        "❌ " +
        (data.error || data.Error || "Failed to delete transaction.")
    );

}
    } catch (error) {

        console.log(
            "Something went wrong while deleting transaction.",
            error
        );

    }

}


const editTransactionForm =
    document.getElementById("editTransactionForm");

if (editTransactionForm) {

    const transaction_id =
        document.getElementById("editTransactionId").value;


    async function loadTransactionForEdit() {

        try {

            const response = await fetch(
                "/transactions",
                {
                    method: "GET"
                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                console.log(
                    data.error || data.Error
                );

                return;
            }


            const transactions =
                data.Transaction;


            let transaction = null;

            transactions.forEach(function(tran) {

                if (
                    tran.transaction_id ==
                    transaction_id
                ) {

                    transaction = tran;

                }

            });


            if (transaction === null) {

                console.log(
                    "Transaction not found."
                );

                return;
            }


            document.getElementById(
                "editTransactionDescription"
            ).value =
                transaction.description;


            document.getElementById(
                "editTransactionAmount"
            ).value =
                transaction.amount;


            document.getElementById(
                "editTransactionType"
            ).value =
                transaction.type;


            document.getElementById(
                "editTransactionDate"
            ).value =
                transaction.transaction_date;


            const currentCategory =
                transaction.category_id;


            await loadCategoriesForEdit(
                currentCategory
            );

        }

        catch (error) {

            console.log(
                "Something went wrong while loading transaction.",
                error
            );

        }

    }


    async function loadCategoriesForEdit(
        currentCategory
    ) {

        const categoryDropdown =
            document.getElementById(
                "editTransactionCategory"
            );


        try {

            const response = await fetch(
                "/categories",
                {
                    method: "GET"
                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                console.log(
                    data.error || data.Error
                );

                return;
            }


            const categories =
                data.Categories;


            categoryDropdown.innerHTML =
                '<option value="">Select Category</option>';


            categories.forEach(function(category) {

                const option =
                    document.createElement("option");


                option.value =
                    category.category_id;


                option.textContent =
                    category.name;


                if (
                    category.category_id ==
                    currentCategory
                ) {

                    option.selected = true;

                }


                categoryDropdown.appendChild(
                    option
                );

            });

        }

        catch (error) {

            console.log(
                "Something went wrong while loading categories.",
                error
            );

        }

    }

    loadTransactionForEdit();
    editTransactionForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const transaction_id =
                document.getElementById(
                    "editTransactionId"
                ).value;


            const amount =
                document.getElementById(
                    "editTransactionAmount"
                ).value;


            const category_id =
                document.getElementById(
                    "editTransactionCategory"
                ).value;


            const type =
                document.getElementById(
                    "editTransactionType"
                ).value;


            const description =
                document.getElementById(
                    "editTransactionDescription"
                ).value;


            const transaction_date =
                document.getElementById(
                    "editTransactionDate"
                ).value;


            try {

                const response =
                    await fetch(
                        `/transactions/${transaction_id}`,
                        {
                            method: "PUT",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({

                                amount:
                                    amount,

                                category_id:
                                    category_id,

                                type:
                                    type,

                                description:
                                    description,

                                transaction_date:
                                    transaction_date

                            })
                        }
                    );


                const data =
                    await response.json();


                

               if (response.ok) {

               alert("✅ " + data.Message);

              window.location.href = "/transactions-page";

            } else {

            alert(
            "❌ " +
            (data.error || data.Mesaage || "Failed to update transaction.")
             );

            }}
            catch (error) {

                console.error(
                    "Error:",
                    error
                );

                alert(
                    "Something went wrong while updating transaction."
                );

            }

        }
    );
}
const transactionClearFilterBtn =
    document.getElementById("transactionClearFilterBtn");

if (transactionClearFilterBtn) {

    transactionClearFilterBtn.addEventListener(
        "click",
        function() {

            document.getElementById(
                "transactionCategoryFilter"
            ).value = "";

            document.getElementById(
                "transactionMonthFilter"
            ).value = "";

            window.location.reload();

        }
    );

}

