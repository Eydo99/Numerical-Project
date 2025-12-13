import { Component, Input, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RootFindingResponse } from '../../services/rootfinding.service';

interface StepData {
  first?: number;
  second?: number;
  point?: number;
  result: number;
  f_result: number;
}

@Component({
  selector: 'app-output',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './output.component.html',
  styleUrls: ['./output.component.css']
})
export class OutputComponent {
  @Input() solution: number | null = null;
  @Input() iterations: number = 0;
  @Input() executionTime: number = 0;
  @Input() steps: StepData[] = [];
  @Input() error: string | null = null;
  @Input() selectedMethod: string = '';
  @Input() convergenceStatus: number | null = null;
  @Input() plotImageUrl: string | null = null;

  showSimulator: boolean = false;
  currentStepIndex: number = 0;

  constructor(private cdr: ChangeDetectorRef) {}

  openSimulator(): void {
    if (this.steps.length === 0) return;
    this.showSimulator = true;
    this.currentStepIndex = 0;
  }

  closeSimulator(): void {
    this.showSimulator = false;
  }

  nextStep(): void {
    if (this.currentStepIndex < this.steps.length - 1) {
      this.currentStepIndex++;
    }
  }

  previousStep(): void {
    if (this.currentStepIndex > 0) {
      this.currentStepIndex--;
    }
  }

  goToStep(index: number): void {
    if (index >= 0 && index < this.steps.length) {
      this.currentStepIndex = index;
    }
  }

  getCurrentStep(): StepData | null {
    return this.steps[this.currentStepIndex] || null;
  }

  getMethodDisplayName(): string {
    const names: { [key: string]: string } = {
      'bisection': 'Bisection Method',
      'false-position': 'False Position Method',
      'fixed-point': 'Fixed Point Iteration',
      'newton-orig': 'Newton-Raphson (Original)',
      'newton-mod': 'Newton-Raphson (Modified)',
      'secant': 'Secant Method'
    };
    return names[this.selectedMethod] || this.selectedMethod;
  }

  getConvergenceStatusText(): string {
    if (this.convergenceStatus === null) return '';
    if (this.convergenceStatus === 1) return '✓ Converged';
    if (this.convergenceStatus === -1) return '✗ Diverged';
    return '⚠ Undetermined';
  }

  getConvergenceStatusClass(): string {
    if (this.convergenceStatus === 1) return 'text-green-600';
    if (this.convergenceStatus === -1) return 'text-red-600';
    return 'text-yellow-600';
  }

  shouldShowIntervalInfo(): boolean {
    return this.selectedMethod === 'bisection' || this.selectedMethod === 'false-position';
  }

  shouldShowPointInfo(): boolean {
    return this.selectedMethod === 'fixed-point' ||
      this.selectedMethod === 'newton-orig' ||
      this.selectedMethod === 'newton-mod';
  }

  shouldShowTwoPoints(): boolean {
    return this.selectedMethod === 'secant';
  }
}
