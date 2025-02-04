/** @odoo-module */

import { registry } from "@web/core/registry"
import { KpiCard } from "./kpi_card/kpi_card"
import { ChartRenderer } from "./chart_renderer/chart_renderer"
import { jsonrpc } from "@web/core/network/rpc_service";
const { Component, onWillStart, useRef, onMounted,useState } = owl

export class OwlPatientDashboard extends Component {
    setup(){

        this.state = useState({
            selectedPeriod: 0,  // Set default to 0
            total_patients: 0,
            male_patient: 0,
            female_patient: 0,
            male_percent: 0,
            female_percent: 0,
            child_patient:0,
            child_percent:0,
        });

    }
    async fetchData(event) {
        const selectedPeriod = parseInt(event.target.value, 10);  // Get the selected value
        
        console.log(selectedPeriod)
        console.log("########################## fetch data ################")

        try {
            console.log("###################### try ########################")
            const data = await jsonrpc("/hospital/patient_dashboard/data", {
                selected_data: selectedPeriod  
            });            
            console.log("####################### data ############",data)


            this.state.total_patients = data.total_patients;
            this.state.male_patient = data.male_patient;
            this.state.female_patient = data.female_patient;
            this.state.male_percent = data.male_percent;
            this.state.female_percent = data.female_percent;
            this.state.child_percent = data.child_percent;
            this.state.child_patient = data.child_patient;

        } catch (error) {
            console.error("Error fetching patient data:", error);
        }
    }
}

OwlPatientDashboard.template = "owl.PatientDashboard"
OwlPatientDashboard.components = { KpiCard, ChartRenderer }

registry.category("actions").add("owl.patient_dashboard", OwlPatientDashboard)