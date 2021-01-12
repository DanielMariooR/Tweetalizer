import React from 'react';
import Chart from 'chart.js';

class BarChart extends React.Component {
	constructor(props){ 
		super(props);
		this.canvasRef = React.createRef();
	}

	componentDidUpdate() {
		this.myChart.data.datasets[0].data = [this.props.positive, this.props.negative]
		this.myChart.update();
	}

	componentDidMount(){
		this.myChart = new Chart(this.canvasRef.current, {
			type: 'bar',
			data: {
				labels: ["Positive", "Negative"],
				datasets: [{
					label: 'Sentiments',
					data: [this.props.positive, this.props.negative],
					backgroundColor: this.props.color
				}]
			},
			options: {
	        maintainAspectRatio: false,
	        scales: {
	          yAxes: [
	            {
	              ticks: {
	                min: 0,
	                max: 100
	              }
	            }
	          ]
	        }
	      }
		});
	}

	render(){
		return <canvas ref={this.canvasRef}/>
	}
}


export default BarChart;