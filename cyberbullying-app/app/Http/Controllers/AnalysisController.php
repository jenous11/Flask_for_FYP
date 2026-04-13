<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use App\Models\Analysis;

class AnalysisController extends Controller
{
    public function index()
    {
        return view('analyze');
    }

    public function analyze(Request $request)
    {
        $request->validate([
            'text' => 'required|string|min:3'
        ]);

        // Call Flask API
        $response = Http::post('http://127.0.0.1:5000/predict', [
            'text' => $request->input('text')
        ]);

        $result = $response->json();

        // Determine severity
        if ($result['label'] === 'Not Cyberbullying') {
            $status = 'Safe';
        } elseif (in_array($result['label'], ['Other Cyberbullying', 'Gender'])) {
            $status = 'Suspicious';
        } else {
            $status = 'Toxic';
        }

        // Save to database
        Analysis::create([
            'input_text' => $request->input('text'),
            'label'      => $result['label'],
            'label_id'   => $result['label_id'],
            'confidence' => $result['confidence'],
            'status'     => $status,
        ]);

        return back()
            ->withInput()
            ->with('result', $result)
            ->with('status', $status);
    }

    public function history()
    {
        $analyses = Analysis::latest()->paginate(15);
        return view('history', compact('analyses'));
    }

    public function dashboard()
    {
        $total    = Analysis::count();
        $bullying = Analysis::where('label_id', '!=', 0)->count();
        $safe     = Analysis::where('label_id', 0)->count();

        $labelCounts = [];
        for ($i = 0; $i < 6; $i++) {
            $labelCounts[$i] = Analysis::where('label_id', $i)->count();
        }

        return view('dashboard', compact('total', 'bullying', 'safe', 'labelCounts'));
    }

    public function about()
    {
        return view('about');
    }

    public function destroy($id)
    {
        Analysis::findOrFail($id)->delete();
        return back()->with('success', 'Record deleted successfully!');
    }
    public function export()
{
    $analyses = Analysis::latest()->get();

    $headers = [
        'Content-Type'        => 'text/csv',
        'Content-Disposition' => 'attachment; filename="cyberguard_history.csv"',
    ];

    $callback = function() use ($analyses) {
        $file = fopen('php://output', 'w');
        fputcsv($file, ['ID', 'Text', 'Label', 'Confidence', 'Status', 'Date']);
        foreach ($analyses as $a) {
            fputcsv($file, [
                $a->id,
                $a->input_text,
                $a->label,
                $a->confidence . '%',
                $a->status,
                $a->created_at->format('M d, Y H:i')
            ]);
        }
        fclose($file);
    };

    return response()->stream($callback, 200, $headers);
}
}