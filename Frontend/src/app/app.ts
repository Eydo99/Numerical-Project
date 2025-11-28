// app.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SolverService } from './solve-service';
import { ChangeDetectorRef } from '@angular/core';
import { interval, Subject, BehaviorSubject } from 'rxjs';
import { takeUntil, takeWhile, map } from 'rxjs/operators';
interface Method {
  id: string;
  name: string;
  description: string;
  icon: string;
}

interface Step {
  type: string;
  answers: number[];
  matrix?: number[][];
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: 'app.html',
  styles: [
    `
      :host {
        display: block;
      }

      input[type='text']::-webkit-outer-spin-button,
      input[type='text']::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
      }
    `,
  ],
})
export class App {
  matrixSize = 3;
  selectedMethod = 'gauss';
  sigFigures = 4;
  maxIterations = 100;
  tolerance = 0.0001;
  luAlgorithm = 'doolittle';
  initialGuess: number[] = Array(this.matrixSize).fill(0);
  matrix: string[][] = [];
  solution: number[] | null = null;
  solutionError: string | null = null;
  executionTime: number = 0;
  iterations: number = 0;
  isLoading = false;
  hasInvalidInput = false;
  invalidInputMessage = '';
  problemMessage = '';
  scaling = false;
  endpoints = {
    gauss: '/solve/gausselim',
    'gauss-jordan': '/solve/gaussjordan',
    cholesky: '/solve/cholesky',
    dolittle: '/solve/dolittle',
    crout: '/solve/crout',
    jacobi: '/solve/jacobi',
    'gauss-siedel': '/solve/gauss_seidel',
  };
  currentEndpoint = this.endpoints['gauss'];

  methods: Method[] = [
    {
      id: 'gauss',
      name: 'Gaussian Elimination',
      description: 'Forward elimination only',
      icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1H5a1 1 0 01-1-1v-3zM14 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1h-4a1 1 0 01-1-1v-3z"></path></svg>',
    },
    {
      id: 'gauss-jordan',
      name: 'Gauss-Jordan',
      description: 'Reduced row echelon form',
      icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>',
    },
    {
      id: 'lu',
      name: 'LU Decomposition',
      description: 'Lower-Upper factorization',
      icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>',
    },
    {
      id: 'jacobi',
      name: 'Jacobi Method',
      description: 'Iterative diagonal method',
      icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>',
    },
    {
      id: 'gauss-seidel',
      name: 'Gauss-Seidel',
      description: 'Improved iterative method',
      icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>',
    },
  ];

  // Step simulator properties
  steps: Step[] = [];
  showSimulator: boolean = false; // Controls visibility
  currentStepIndex$ = new BehaviorSubject<number>(0);
  isPlaying$ = new BehaviorSubject<boolean>(false);
  playbackSpeed: number = 1000; // ms between steps

  private stopPlayback$ = new Subject<void>();

  validateInput(): void {
    const validNumberPattern = /^-?\d*\.?\d+(e[+-]?\d+)?$/i;

    this.hasInvalidInput = false;
    this.invalidInputMessage = '';

    for (let i = 0; i < this.matrix.length; i++) {
      for (let j = 0; j < this.matrix[i].length; j++) {
        const value = this.matrix[i][j].trim();

        // empty cells
        if (value === '' || value === '-') {
          continue;
        }

        if (!validNumberPattern.test(value)) {
          this.hasInvalidInput = true;
          this.invalidInputMessage = `Invalid input `;

          return;
        }
      }
    }

    // Check initial guess for iterative methods
    if (this.selectedMethod === 'jacobi' || this.selectedMethod === 'gauss-seidel') {
      for (let i = 0; i < this.initialGuess.length; i++) {
        const value = this.initialGuess[i];

        if (!value) {
          continue;
        }
      }
    }
  }

  constructor(private solverService: SolverService, private cdr: ChangeDetectorRef) {
    this.initializeMatrix();
    this.initializeGuess();
  }

  initializeMatrix(): void {
    this.matrix = Array(this.matrixSize)
      .fill(null)
      .map(() => Array(this.matrixSize + 1).fill(''));
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
        ['1', '3', '8'],
      ];
    } else if (this.matrixSize === 3) {
      this.matrix = [
        ['2', '1', '-1', '8'],
        ['-3', '-1', '2', '-11'],
        ['-2', '1', '2', '-3'],
      ];
    } else if (this.matrixSize === 4) {
      this.matrix = [
        ['2', '1', '-1', '1', '4'],
        ['1', '2', '1', '-1', '1'],
        ['3', '-1', '2', '1', '10'],
        ['1', '1', '1', '2', '6'],
      ];
    } else if (this.matrixSize === 5) {
      this.matrix = [
        ['2', '1', '0', '0', '1', '5'],
        ['1', '3', '1', '0', '0', '8'],
        ['0', '1', '4', '1', '0', '12'],
        ['0', '0', '1', '3', '1', '10'],
        ['1', '0', '0', '1', '2', '7'],
      ];
    } else if (this.matrixSize === 8) {
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
    }
  }

  clearMatrix(): void {
    this.initializeMatrix();
    this.solution = null;
    this.solutionError = null;
    this.executionTime = 0;
    this.iterations = 0;
  }

  trackByIndex(index: number): number {
    return index;
  }

  solveSystem(): void {
    this.validateInput();
    console.log(this.matrix);

    if (this.hasInvalidInput) {
      return;
    }

    //reload
    this.isLoading = true;
    this.solution = null;
    this.solutionError = null;
    this.executionTime = 0;
    this.problemMessage = '';
    this.steps = [];
    this.showSimulator = false

    switch (this.selectedMethod) {
      case 'gauss':
        this.currentEndpoint = this.endpoints['gauss'];
        break;
      case 'gauss-jordan':
        this.currentEndpoint = this.endpoints['gauss-jordan'];
        break;
      case 'jacobi':
        this.currentEndpoint = this.endpoints['jacobi'];
        break;
      case 'gauss-siedel':
        this.currentEndpoint = this.endpoints['gauss-siedel'];
        break;
      case 'lu': {
        switch (this.luAlgorithm) {
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
    console.log('initialGuess : ' + this.initialGuess);
    console.log(
      'SELECTED METHOD : ' +
        this.selectedMethod +
        ' ' +
        (this.selectedMethod === 'lu' ? this.luAlgorithm : '')
    );

    this.solverService
      .getSolution(
        this.matrixSize,
        this.matrix,
        this.sigFigures,
        this.maxIterations,
        this.tolerance,
        this.initialGuess,
        this.scaling,
        this.currentEndpoint
      )
      .subscribe({
        next: (res) => {
          console.log('MATRIX A :' + this.solution);
          console.log(res.steps);
          console.log(res.result);
          if (!res.result) {
            console.log(res.flags.singular);
            if (res.flags.singular) this.solutionError = 'MATRIX IS SINGULAR , NO UNIQUE SOLUTION';
            else if (res.flags.asymmetric)
              this.solutionError = 'MATRIX IS ASYMMETRIC , NO SOLUTION';
            else if (res.flags.positive_indef)
              this.solutionError = "MATRIX ISN'T Positive Definite , NO SOLUTION";
            else this.solutionError = 'NO SOLUTION';
          } else {
            this.solution = res.result;
            this.executionTime = res.exec_time * 1000 || 0;
            this.iterations = res.itr_cnt || 0;
            this.steps = res.steps || [];
          }
          if (res.flags?.conv === false) {
            //console.log(res.flags.conv);
            this.problemMessage =
              "(THE MATRIX ISN'T DIAGONALLY DOMINANT , THE SOLUTION MAY NOT CONVERGE)";
          }
          this.isLoading = false;

          this.isLoading = false;

          this.isLoading = false;

          this.cdr.detectChanges(); // Manually trigger change detection
        },
        error: (err) => {
          this.solutionError = 'Error solving system';
          this.isLoading = false;
          this.cdr.detectChanges();
        },
      });
  }

  

  
  shouldShowScalingOption(): boolean {
    return (
      this.selectedMethod === 'gauss' ||
      this.selectedMethod === 'gauss-jordan' ||
      (this.selectedMethod === 'lu' && this.luAlgorithm === 'dolittle')
    );
  }

  openSimulator(): void {
    if (this.steps.length === 0) {
      console.warn('No steps available to simulate');
      return;
    }

    console.log('Opening simulator for method:', this.selectedMethod);
    console.log('First step:', this.steps[0]);

    this.showSimulator = true;
    this.resetSimulation();
  }

  // Close the simulator
  closeSimulator(): void {
    this.stopPlayback();
    this.showSimulator = false;
  }

  // Step simulator controls
  playSimulation(): void {
    if (this.steps.length === 0) return;

    this.isPlaying$.next(true);
    const startIndex = this.currentStepIndex$.value;

    interval(this.playbackSpeed)
      .pipe(
        takeUntil(this.stopPlayback$),
        map((count) => startIndex + count + 1),
        takeWhile((index) => index < this.steps.length)
      )
      .subscribe({
        next: (index) => {
          this.currentStepIndex$.next(index);
          this.cdr.detectChanges();
        },
        complete: () => {
          this.isPlaying$.next(false);
          this.cdr.detectChanges();
        },
      });
  }

  pauseSimulation(): void {
    this.stopPlayback();
    this.isPlaying$.next(false);
  }

  stopPlayback(): void {
    this.stopPlayback$.next();
  }

  nextStep(): void {
    const current = this.currentStepIndex$.value;
    if (current < this.steps.length - 1) {
      this.currentStepIndex$.next(current + 1);
    }
  }

  previousStep(): void {
    const current = this.currentStepIndex$.value;
    if (current > 0) {
      this.currentStepIndex$.next(current - 1);
    }
  }

  goToStep(index: number): void {
    if (index >= 0 && index < this.steps.length) {
      this.stopPlayback();
      this.currentStepIndex$.next(index);
    }
  }

  resetSimulation(): void {
    this.stopPlayback();
    this.currentStepIndex$.next(0);
  }

  goToEnd(): void {
    this.stopPlayback();
    this.currentStepIndex$.next(this.steps.length - 1);
  }

  setPlaybackSpeed(speed: number): void {
    this.playbackSpeed = speed;
    const wasPlaying = this.isPlaying$.value;

    if (wasPlaying) {
      this.stopPlayback();
      this.playSimulation();
    }
  }

  // Add this method to your component class
  shouldShowSimulator(): boolean {
    // Don't show simulator for LU decomposition methods
    if (this.selectedMethod === 'lu') {
      return false;
    }
    return this.steps && this.steps.length > 0;
  }

  // Add this method to check if we should show matrix
  shouldShowMatrix(): boolean {
    return this.selectedMethod === 'gauss' || this.selectedMethod === 'gauss-jordan';
  }

  // Update getCurrentStep to handle matrix display
  getCurrentStep(): Step | null {
    const index = this.currentStepIndex$.value;
    return this.steps[index] || null;
  }
  ngOnDestroy(): void {
    this.stopPlayback();
    this.stopPlayback$.complete();
    this.currentStepIndex$.complete();
    this.isPlaying$.complete();
  }
}
