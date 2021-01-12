import logo from './logo.svg';
import './App.css';
import React, {useState} from 'react';
import axios from 'axios';
import BarChart from './components/BarChart';

let axiosConfig = {
  headers: {
      'Content-Type' : 'application/json; charset=UTF-8',
      'Accept': 'Token',
      "Access-Control-Allow-Origin": "*",
  }
};


class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {topic: '', positive: 0, negative: 0, topics: ''};
    this.handleInput = this.handleInput.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleInput = (e) => {
    this.setState({
      topic: e.target.value
    });
  }

  handleSubmit = (e) => {
    e.preventDefault();
    axios
      .post('/home', {
        topic: JSON.stringify(this.state.topic)
      }, axiosConfig)
      .then((res) => {
        this.setState ({
          topic: ""
        })
      })
      .catch((err) => {})
  }

  componentDidMount(){
    axios.get('/result')
    .then(({data}) => {
      this.setState({
        positive: data.positive,
        negative: data.negative,
        topics: data.topic
      });
    })
    .catch(err => {})
  }

  
  render(){
    const positive = this.state.positive;
    const negative = this.state.negative;
    return (
      <div>
        <h1> Twitter Sentiment Analyzer </h1>
        <form onSubmit={this.handleSubmit}>
          <label> Topic: <input type="text" value={this.state.topic} onChange={this.handleInput}/></label>
          <input type="submit" value="Submit"/>
        </form>
        <p>Positive: {positive}</p>
        <p>Negative: {negative}</p>

        <BarChart
          positive={positive}
          negative={negative}
          color="#70CAD1"
        />
      </div>
      );
  }
}


export default App;
