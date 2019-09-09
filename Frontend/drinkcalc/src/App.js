import React, { Component } from 'react';
import './App.css';

export class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      drinks: [],
      currentDrink: 1,
      weight: 0,
      gender: 'm',
      time: 0,
      alcoholLevel: 0
    }
  }
  componentDidMount() {
    fetch('http://localhost:5000/drinks')
      .then(data => data.json())
      .then((data) => { this.setState({ drinks: data }) });
  }

  onSelectDrink = e => {
    this.setState({ currentDrink: e.target.value });
  }

  onSelectGender = e => {
    this.setState({ gender: e.target.value });
  }

  onSubmit = e => {
    e.preventDefault();
    fetch('http://localhost:5000/calculateBAC?drinkId=' + this.state.currentDrink + '&weight=' + this.state.weight + '&gender=' + this.state.gender + '&time=' + this.state.time)
      .then(data => data.json())
      .then((data) => { this.setState({ alcoholLevel: data }); });
  }

  handleWeightChange = e => {
    this.setState({ weight: e.target.value });
  }
  handleTimeChange = e => {
    this.setState({ time: e.target.value });
  }

  render() {

    return (
      <div style={{ alignItems: 'center', justifyContent: 'center', display: 'flex', }}>
        <form onSubmit={this.onSubmit}>
          <br />
          <label>
            Contenido de Alcohol en la Sangre:
          </label>
          <br />
          <label>
            {this.state.alcoholLevel}
          </label>
          <br />
          <label>
            Seleccione una bebida: &nbsp;
            <br />
            <select onChange={this.onSelectDrink}>
              {Object.keys(this.state.drinks).map((key) => (

                <option value={this.state.drinks[key].drink_id}>{this.state.drinks[key].drink_name}</option>
              ))}
            </select>
          </label>
          <br />
          <label>Digite su peso (libras): &nbsp;</label>
          <br />
          <input name="weight" onChange={this.handleWeightChange}></input>
          <br />
          <label>Seleccione su sexo: &nbsp;</label>
          <br />
          <select onChange={this.onSelectGender}>
            <option value="m">Masculino</option>
            <option value="f">Femenino</option>
          </select>
          <br />
          <label>Hace cuanto tiempo dejo de beber? (en horas): &nbsp;</label>
          <br />
          <input name="time" onChange={this.handleTimeChange}></input>
          <br />
          <br />

          <input type="submit" value="Calcular BAC " />
        </form>

      </div>
    );
  }
}



export default App;
