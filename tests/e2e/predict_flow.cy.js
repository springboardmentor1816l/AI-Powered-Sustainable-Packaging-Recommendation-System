describe("EcoPackAI – End-to-End Flow", () => {

  it("Loads homepage", () => {
    cy.visit("http://localhost:3000");
    cy.contains("EcoPackAI");
  });

  it("Submits product form", () => {
    cy.get("#product_name").type("Glass Bottle");
    cy.get("#category").select("Food");
    cy.get("#product_weight").type("0.75");
    cy.get("#fragility_index").invoke("val", 4).trigger("change");
    cy.get("#shipping_type").select("Road");
    cy.contains("Generate Recommendation").click();
  });

  it("Shows loader", () => {
    cy.contains("Running AI inference").should("exist");
  });

  it("Displays recommendations", () => {
    cy.get("table").should("exist");
    cy.get("tbody tr").should("have.length.at.least", 1);
  });

  it("Renders charts", () => {
    cy.get("#costCo2Chart").should("exist");
    cy.get("#sustainabilityGauge").should("exist");
  });

  it("Exports CSV & PDF", () => {
    cy.contains("Export CSV").click();
    cy.contains("Download PDF").click();
  });

});
