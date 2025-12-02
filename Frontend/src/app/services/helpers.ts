import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class Helpers {
  private baseUrl = 'http://127.0.0.1:8080';
  currentEndpoint = 'http://127.0.0.1:8080/solve/gauss';
  matrix : string[][] = []; 
  endpoints = {
    gauss: '/solve/gausselim',
    'gauss-jordan': '/solve/gaussjordan',
    cholesky: '/solve/cholesky',
    dolittle: '/solve/dolittle',
    crout: '/solve/crout',
    jacobi: '/solve/jacobi',
    'gauss-seidel': '/solve/gauss_seidel',
  };

  getEndpoint(selectedMethod: string, luAlgorithm: string): string {
    switch (selectedMethod) {
      case 'gauss':
        this.currentEndpoint = this.endpoints['gauss'];
        break;
      case 'gauss-jordan':
        this.currentEndpoint = this.endpoints['gauss-jordan'];
        break;
      case 'jacobi':
        this.currentEndpoint = this.endpoints['jacobi'];
        break;
      case 'gauss-seidel':
        this.currentEndpoint = this.endpoints['gauss-seidel'];
        break;
      case 'lu': {
        switch (luAlgorithm) {
          case 'dolittle':
            this.currentEndpoint = this.endpoints['dolittle'];
            break;
          case 'cholesky':
            this.currentEndpoint = this.endpoints['cholesky'];
            break;
          case 'crout':
            this.currentEndpoint = this.endpoints['crout'];
            break;
        }
        break;
      }
    }

    return this.currentEndpoint ;
  }


  loadExample(matrixSize : number): string[][] {
    switch (matrixSize) {
      case 2:
        this.matrix = [
          ['2', '1', '5'],
          ['1', '3', '8'],
        ];
        break;

      case 3:
        this.matrix = [
          ['2', '1', '-1', '8'],
          ['-3', '-1', '2', '-11'],
          ['-2', '1', '2', '-3'],
        ];
        break;

      case 4:
        this.matrix = [
          ['2', '1', '-1', '1', '4'],
          ['1', '2', '1', '-1', '1'],
          ['3', '-1', '2', '1', '10'],
          ['1', '1', '1', '2', '6'],
        ];
        break;

      case 5:
        this.matrix = [
          ['2', '1', '0', '0', '1', '5'],
          ['1', '3', '1', '0', '0', '8'],
          ['0', '1', '4', '1', '0', '12'],
          ['0', '0', '1', '3', '1', '10'],
          ['1', '0', '0', '1', '2', '7'],
        ];
        break;
      case 6:
        [
          ['4', '1', '0', '0', '1', '0', '18'],
          ['1', '5', '1', '0', '0', '1', '22'],
          ['0', '1', '4', '1', '0', '0', '17'],
          ['0', '0', '1', '5', '1', '0', '23'],
          ['1', '0', '0', '1', '3', '1', '16'],
          ['0', '1', '0', '0', '1', '4', '19'],
        ];
        break;

      case 7:
        this.matrix = [
          ['3', '1', '0', '0', '1', '0', '0', '14'],
          ['1', '4', '1', '0', '0', '1', '0', '20'],
          ['0', '1', '5', '1', '0', '0', '1', '26'],
          ['0', '0', '1', '4', '1', '0', '0', '18'],
          ['1', '0', '0', '1', '3', '1', '0', '15'],
          ['0', '1', '0', '0', '1', '4', '1', '19'],
          ['0', '0', '1', '0', '0', '1', '3', '17'],
        ];
        break;

      case 8:
        this.matrix = [
          ['2', '1', '0', '0', '1', '0', '0', '0', '10'],
          ['1', '3', '1', '0', '0', '1', '0', '0', '15'],
          ['0', '1', '4', '1', '0', '0', '1', '0', '20'],
          ['0', '0', '1', '3', '1', '0', '0', '1', '18'],
          ['1', '0', '0', '1', '2', '1', '0', '0', '12'],
          ['0', '1', '0', '0', '1', '3', '1', '0', '17'],
          ['0', '0', '1', '0', '0', '1', '4', '1', '22'],
          ['0', '0', '0', '1', '0', '0', '1', '3', '19'],
        ];
        break;
    }

    return this.matrix ;
  }


}
