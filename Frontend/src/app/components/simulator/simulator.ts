import { Component, EventEmitter, Output, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AsyncPipe } from '@angular/common';
import { interval, Subject, BehaviorSubject } from 'rxjs';
import { takeUntil, takeWhile, map } from 'rxjs/operators';
import { ChangeDetectorRef } from '@angular/core';
interface Step {
  type: string;
  answers: number[];
  matrix?: number[][];
  L?: number[][];
  U?: number[][];
}
@Component({
  selector: 'app-simulator',
  imports: [AsyncPipe, CommonModule],
  templateUrl: './simulator.html',
  styleUrl: './simulator.css',
})
export class Simulator {
  showSimulator: boolean = false; // Controls visibility

  currentStepIndex$ = new BehaviorSubject<number>(0);
  isPlaying$ = new BehaviorSubject<boolean>(false);
  playbackSpeed: number = 1000; // ms between steps
  private stopPlayback$ = new Subject<void>();

  @Input() selectedMethod: string = 'gauss';
  @Input() luAlgorithm: string = 'dolittle';
  @Input() steps: Step[] = [];
  @Output() visibilityChange = new EventEmitter<boolean>();
  constructor(private cdr: ChangeDetectorRef) {}

  openSimulator(): void {
    if (this.steps.length === 0) {
      console.warn('No steps available to simulate');
      return;
    }

    console.log('Opening simulator for method:', this.selectedMethod);
    console.log('First step:', this.steps[0]);

    this.showSimulator = true;
    this.visibilityChange.emit(this.showSimulator);
    this.resetSimulation();
  }

  // Close the simulator
  closeSimulator(): void {
    this.stopPlayback();
    this.showSimulator = false;
    this.visibilityChange.emit(this.showSimulator)
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

  // booleans
  shouldShowSimulatorButton(): boolean {
    
    if (this.selectedMethod === 'lu' && this.luAlgorithm != 'dolittle') {
      return false;
    }
    return this.steps && this.steps.length > 0;
  }

  // Add this method to check if we should show matrix
  shouldShowMatrix(): boolean {
    return this.selectedMethod === 'gauss' || this.selectedMethod === 'gauss-jordan';
  }
  shouldShowLU(): boolean {
    return this.selectedMethod === 'lu' && this.luAlgorithm === 'dolittle';
  }

  // matrix step
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
