@extends('layouts.app')

@section('content')

<div class="max-w-2xl mx-auto">

    <!-- Title -->
    <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-white mb-2">🛡️ Cyberbullying Detector</h1>
        <p class="text-gray-400">Paste any text below to analyze it for cyberbullying content</p>
    </div>

    <!-- Input Form -->
    <div class="bg-gray-900 rounded-2xl p-6 border border-gray-800">
        <form method="POST" action="/analyze">
            @csrf
            <textarea
                name="text"
                rows="5"
                placeholder="Type or paste text here to analyze..."
                class="w-full bg-gray-800 text-white border border-gray-700 rounded-xl p-4 text-sm focus:outline-none focus:ring-2 focus:ring-red-500 resize-none"
            >{{ old('text') }}</textarea>

            @error('text')
                <p class="text-red-400 text-sm mt-2">{{ $message }}</p>
            @enderror

            <button type="submit"
                class="mt-4 w-full bg-red-600 hover:bg-red-700 text-white font-semibold py-3 rounded-xl transition">
                🔍 Analyze Text
            </button>
        </form>
    </div>

    <!-- Result Card -->
    @if(session('result'))
    @php
        $result = session('result');
        $status = session('status');
        $colors = [
            'Not Cyberbullying'   => 'emerald',
            'Gender'              => 'purple',
            'Religion'            => 'orange',
            'Other Cyberbullying' => 'blue',
            'Age'                 => 'red',
            'Ethnicity'           => 'pink',
        ];
        $color = $colors[$result['label']] ?? 'gray';
    @endphp

    <div class="mt-6 bg-gray-900 rounded-2xl p-6 border border-gray-800">
        <h2 class="text-lg font-bold mb-4 text-white">📊 Analysis Result</h2>

        <!-- Label Badge -->
        <div class="flex items-center gap-3 mb-4">
            <span class="text-gray-400 text-sm">Detected:</span>
            <span class="px-3 py-1 rounded-full text-sm font-semibold
                @if($result['label'] == 'Not Cyberbullying') bg-emerald-900 text-emerald-300
                @elseif($result['label'] == 'Gender') bg-purple-900 text-purple-300
                @elseif($result['label'] == 'Religion') bg-orange-900 text-orange-300
                @elseif($result['label'] == 'Age') bg-red-900 text-red-300
                @elseif($result['label'] == 'Ethnicity') bg-pink-900 text-pink-300
                @else bg-blue-900 text-blue-300
                @endif">
                {{ $result['label'] }}
            </span>
            <span class="text-gray-400 text-sm">{{ $result['confidence'] }}% confidence</span>
        </div>

        <!-- All Probabilities -->
        <div class="space-y-2">
            @foreach($result['all_probs'] as $label => $prob)
            <div class="flex items-center gap-3">
                <span class="text-gray-400 text-xs w-40">{{ $label }}</span>
                <div class="flex-1 bg-gray-800 rounded-full h-2">
                    <div class="bg-red-500 h-2 rounded-full" style="width: {{ $prob }}%"></div>
                </div>
                <span class="text-gray-300 text-xs w-12 text-right">{{ $prob }}%</span>
            </div>
            @endforeach
        </div>
    </div>
    @endif

</div>

@endsection