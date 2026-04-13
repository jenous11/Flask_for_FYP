@extends('layouts.app')

@section('content')

<div class="mb-8">
    <h1 class="text-3xl font-bold text-white">Dashboard</h1>
    <p class="text-gray-400 mt-1 text-sm mono">Overview of all cyberbullying detections</p>
</div>

<!-- Stats Cards -->
<div class="grid grid-cols-3 gap-6 mb-8">
    <div class="bg-gray-900 border border-gray-800 rounded-2xl p-6">
        <p class="text-gray-400 text-sm mono uppercase tracking-wider mb-2">Total Analyzed</p>
        <p class="text-4xl font-bold text-white">{{ $total }}</p>
        <p class="text-gray-500 text-xs mt-2">All time</p>
    </div>
    <div class="bg-gray-900 border border-red-900/40 rounded-2xl p-6">
        <p class="text-gray-400 text-sm mono uppercase tracking-wider mb-2">Bullying Detected</p>
        <p class="text-4xl font-bold text-red-400">{{ $bullying }}</p>
        <p class="text-gray-500 text-xs mt-2">
            @if($total > 0) {{ round(($bullying / $total) * 100, 1) }}% of total @else 0% of total @endif
        </p>
    </div>
    <div class="bg-gray-900 border border-emerald-900/40 rounded-2xl p-6">
        <p class="text-gray-400 text-sm mono uppercase tracking-wider mb-2">Safe Content</p>
        <p class="text-4xl font-bold text-emerald-400">{{ $safe }}</p>
        <p class="text-gray-500 text-xs mt-2">
            @if($total > 0) {{ round(($safe / $total) * 100, 1) }}% of total @else 0% of total @endif
        </p>
    </div>
</div>

<!-- Category Breakdown -->
<div class="grid grid-cols-2 gap-6">

    <!-- Bar Chart -->
    <div class="bg-gray-900 border border-gray-800 rounded-2xl p-6">
        <h2 class="text-lg font-bold text-white mb-6">Category Breakdown</h2>
        @php
            $labels = [
                0 => ['name' => 'Not Cyberbullying', 'color' => 'bg-emerald-500'],
                1 => ['name' => 'Gender',             'color' => 'bg-purple-500'],
                2 => ['name' => 'Religion',           'color' => 'bg-orange-500'],
                3 => ['name' => 'Other',              'color' => 'bg-blue-500'],
                4 => ['name' => 'Age',                'color' => 'bg-red-500'],
                5 => ['name' => 'Ethnicity',          'color' => 'bg-pink-500'],
            ];
            $maxCount = max(array_values($labelCounts) ?: [1]);
        @endphp
        <div class="space-y-4">
            @foreach($labels as $id => $info)
            <div class="flex items-center gap-3">
                <span class="text-gray-400 text-xs w-36 truncate">{{ $info['name'] }}</span>
                <div class="flex-1 bg-gray-800 rounded-full h-2.5">
                    <div class="{{ $info['color'] }} h-2.5 rounded-full transition-all duration-700"
                         style="width: {{ $maxCount > 0 ? round(($labelCounts[$id] / $maxCount) * 100) : 0 }}%">
                    </div>
                </div>
                <span class="text-gray-300 mono text-xs w-8 text-right">{{ $labelCounts[$id] }}</span>
            </div>
            @endforeach
        </div>
    </div>

    <!-- Donut Summary -->
    <div class="bg-gray-900 border border-gray-800 rounded-2xl p-6">
        <h2 class="text-lg font-bold text-white mb-6">Safety Overview</h2>
        @if($total > 0)
        @php
            $safePercent     = round(($safe / $total) * 100, 1);
            $bullyingPercent = round(($bullying / $total) * 100, 1);
            $circumference   = 2 * M_PI * 54;
            $safeDash        = ($safePercent / 100) * $circumference;
        @endphp
        <div class="flex items-center justify-center mb-6">
            <div class="relative">
                <svg width="140" height="140" viewBox="0 0 140 140">
                    <circle cx="70" cy="70" r="54" fill="none" stroke="#1f2937" stroke-width="16"/>
                    <circle cx="70" cy="70" r="54" fill="none" stroke="#ef4444" stroke-width="16"
                            stroke-dasharray="{{ $circumference }}" stroke-dashoffset="0"
                            stroke-linecap="round" transform="rotate(-90 70 70)"/>
                    <circle cx="70" cy="70" r="54" fill="none" stroke="#22c55e" stroke-width="16"
                            stroke-dasharray="{{ $safeDash }} {{ $circumference }}"
                            stroke-dashoffset="0"
                            stroke-linecap="round" transform="rotate(-90 70 70)"/>
                    <text x="70" y="65" text-anchor="middle" fill="white" font-size="18" font-weight="bold">{{ $safePercent }}%</text>
                    <text x="70" y="82" text-anchor="middle" fill="#6b7280" font-size="10">Safe</text>
                </svg>
            </div>
        </div>
        <div class="flex justify-center gap-8">
            <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full bg-emerald-500"></span>
                <span class="text-gray-400 text-sm">Safe {{ $safePercent }}%</span>
            </div>
            <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full bg-red-500"></span>
                <span class="text-gray-400 text-sm">Bullying {{ $bullyingPercent }}%</span>
            </div>
        </div>
        @else
        <div class="flex items-center justify-center h-40 text-gray-500">
            No data yet — start analyzing!
        </div>
        @endif
    </div>

</div>

@endsection
