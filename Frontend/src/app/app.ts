// app.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface Method {
  id: string;
  name: string;
  description: string;
  icon: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl:'app.html',
  styles: [`
    :host {
      display: block;
    }
    
    input[type="text"]::-webkit-outer-spin-button,
    input[type="text"]::-webkit-inner-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }
  `]
})
export class App {
  matrixSize = 3;
  selectedMethod = 'gaussian';
  precision = 4;
  maxIterations = 100;
  tolerance = 0.0001;
  luAlgorithm = 'doolittle';
  initialGuess: string[] = [];
  matrix: string[][] = [];
  solution: number[] | null = null;
  solutionError: string | null = null;
  executionTime: number = 0;
  iterations: number = 0;
  isLoading = false;

  methods: Method[] = [
    {
      id: 'gaussian',
      name: 'Gaussian Elimination',
      description: 'Forward elimination only',
      icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1H5a1 1 0 01-1-1v-3zM14 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1h-4a1 1 0 01-1-1v-3z"></path></svg>'
    },
    {
      id: 'gauss-jordan',
      name: 'Gauss-Jordan',
      description: 'Reduced row echelon form',
      icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>'
    },
    {
      id: 'lu',
      name: 'LU Decomposition',
      description: 'Lower-Upper factorization',
      icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>'
    },
    {
      id: 'jacobi',
      name: 'Jacobi Method',
      description: 'Iterative diagonal method',
      icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>'
    },
    {
      id: 'gauss-seidel',
      name: 'Gauss-Seidel',
      description: 'Improved iterative method',
      icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>'
    }
  ];

  constructor() {
    this.initializeMatrix();
    this.initializeGuess();
  }

  initializeMatrix(): void {
    this.matrix = Array(this.matrixSize).fill(null).map(() => 
      Array(this.matrixSize + 1).fill('')
    );
  }

  initializeGuess(): void {
    this.initialGuess = Array(this.matrixSize).fill('0');
  }

  handleSizeChange(size: number): void {
    this.matrixSize = size;
    this.initializeMatrix();
    this.initializeGuess();
    this.solution = null;
    this.solutionError = null;
    this.executionTime = 0;
    this.iterations = 0;
  }

  loadExample(): void {
    if (this.matrixSize === 2) {
      this.matrix = [
        ['2', '1', '5'],
        ['1', '3', '8']
      ];
    } else if (this.matrixSize === 3) {
      this.matrix = [
        ['2', '1', '-1', '8'],
        ['-3', '-1', '2', '-11'],
        ['-2', '1', '2', '-3']
      ];
    } else if (this.matrixSize === 4) {
      this.matrix = [
        ['2', '1', '-1', '1', '4'],
        ['1', '2', '1', '-1', '1'],
        ['3', '-1', '2', '1', '10'],
        ['1', '1', '1', '2', '6']
      ];
    } else if (this.matrixSize === 5) {
      this.matrix = [
        ['2', '1', '0', '0', '1', '5'],
        ['1', '3', '1', '0', '0', '8'],
        ['0', '1', '4', '1', '0', '12'],
        ['0', '0', '1', '3', '1', '10'],
        ['1', '0', '0', '1', '2', '7']
      ];
    }
  }

  clearMatrix(): void {
    this.initializeMatrix();
    this.solution = null;
    this.solutionError = null;
    this.executionTime = 0;
    this.iterations = 0;
  }

  solveSystem(): void {
    this.isLoading = true;

    
    /* setTimeout(() => {
      // Placeholder: return all zeros for testing
      // Replace this with your backend service call
      const n = this.matrixSize;
      this.solution = Array(n).fill(0);
      this.solutionError = null;
      this.executionTime = 0;
      this.iterations = 0;
      this.isLoading = false;
    }, 0); */
  }
}