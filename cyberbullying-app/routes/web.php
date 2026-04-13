<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AnalysisController;

Route::get('/', [AnalysisController::class, 'index'])->name('analyze');
Route::post('/analyze', [AnalysisController::class, 'analyze'])->name('analyze.post');
Route::get('/history', [AnalysisController::class, 'history'])->name('history');
Route::get('/dashboard', [AnalysisController::class, 'dashboard'])->name('dashboard');
Route::get('/about', [AnalysisController::class, 'about'])->name('about');
Route::delete('/history/{id}', [AnalysisController::class, 'destroy'])->name('history.delete');
Route::get('/history/export', [AnalysisController::class, 'export'])->name('history.export');