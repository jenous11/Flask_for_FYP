@extends('layouts.app')

@section('content')

<div class="mb-8 flex items-center justify-between">
    <div>
        <h1 class="text-3xl font-bold text-white">Analysis History</h1>
        <p class="text-gray-400 mt-1 text-sm mono">All previously analyzed texts</p>
    </div>
    <div class="flex gap-3">
        <a href="/history/export" class="bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-semibold px-4 py-2 rounded-xl transition">
            📥 Export CSV
        </a>
        <a href="/" class="bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold px-4 py-2 rounded-xl transition">
            + New Analysis
        </a>
    </div>
</div>

{{-- Success message --}}
@if(session('success'))
<div class="mb-4 px-4 py-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-sm">
    ✅ {{ session('success') }}
</div>
@endif

@if($analyses->count() > 0)
<div class="bg-gray-900 rounded-2xl border border-gray-800 overflow-hidden">
    <table class="w-full text-sm">
        <thead>
            <tr class="border-b border-gray-800 bg-gray-950">
                <th class="text-left px-6 py-4 text-gray-400 font-medium mono text-xs uppercase tracking-wider">Text</th>
                <th class="text-left px-6 py-4 text-gray-400 font-medium mono text-xs uppercase tracking-wider">Label</th>
                <th class="text-left px-6 py-4 text-gray-400 font-medium mono text-xs uppercase tracking-wider">Confidence</th>
                <th class="text-left px-6 py-4 text-gray-400 font-medium mono text-xs uppercase tracking-wider">Status</th>
                <th class="text-left px-6 py-4 text-gray-400 font-medium mono text-xs uppercase tracking-wider">Date</th>
                <th class="text-left px-6 py-4 text-gray-400 font-medium mono text-xs uppercase tracking-wider">Action</th>
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-800">
            @foreach($analyses as $analysis)
            <tr class="hover:bg-gray-800/50 transition">
                <td class="px-6 py-4 max-w-xs">
                    <p class="truncate cursor-pointer hover:text-cyan-400 transition"
                        onclick="this.classList.toggle('truncate')"
                        title="Click to expand">
                        {{ $analysis->input_text }}
                    </p>
                </td>
                <td class="px-6 py-4">
                    <span class="px-2.5 py-1 rounded-full text-xs font-semibold
                        @if($analysis->label == 'Not Cyberbullying') bg-emerald-900/60 text-emerald-300 border border-emerald-700
                        @elseif($analysis->label == 'Gender') bg-purple-900/60 text-purple-300 border border-purple-700
                        @elseif($analysis->label == 'Religion') bg-orange-900/60 text-orange-300 border border-orange-700
                        @elseif($analysis->label == 'Age') bg-red-900/60 text-red-300 border border-red-700
                        @elseif($analysis->label == 'Ethnicity') bg-pink-900/60 text-pink-300 border border-pink-700
                        @else bg-blue-900/60 text-blue-300 border border-blue-700
                        @endif">
                        {{ $analysis->label }}
                    </span>
                </td>
                <td class="px-6 py-4">
                    <span class="mono text-gray-300">{{ $analysis->confidence }}%</span>
                </td>
                <td class="px-6 py-4">
                    <span class="flex items-center gap-1.5 text-xs font-medium
                        @if($analysis->status == 'Safe') text-emerald-400
                        @elseif($analysis->status == 'Suspicious') text-amber-400
                        @else text-red-400
                        @endif">
                        <span class="w-1.5 h-1.5 rounded-full
                            @if($analysis->status == 'Safe') bg-emerald-400
                            @elseif($analysis->status == 'Suspicious') bg-amber-400
                            @else bg-red-400
                            @endif">
                        </span>
                        {{ $analysis->status }}
                    </span>
                </td>
                <td class="px-6 py-4 text-gray-500 mono text-xs">
                    {{ $analysis->created_at->format('M d, Y H:i') }}
                </td>
                <td class="px-6 py-4">
                    <form method="POST" action="/history/{{ $analysis->id }}">
                        @csrf
                        @method('DELETE')
                        <button type="submit"
                            onclick="return confirm('Delete this record?')"
                            class="text-red-400 hover:text-red-300 text-xs border border-red-500/20 hover:border-red-500/40 px-2.5 py-1 rounded-lg transition">
                            🗑️ Delete
                        </button>
                    </form>
                </td>
            </tr>
            @endforeach
        </tbody>
    </table>
</div>

<!-- Pagination -->
<div class="mt-6">
    {{ $analyses->links() }}
</div>

@else
<div class="bg-gray-900 rounded-2xl border border-gray-800 p-16 text-center">
    <div class="text-5xl mb-4">📭</div>
    <h3 class="text-xl font-bold text-white mb-2">No analyses yet</h3>
    <p class="text-gray-400 mb-6">Start analyzing text to see your history here.</p>
    <a href="/" class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2.5 rounded-xl transition">
        Analyze Text
    </a>
</div>
@endif

@endsection