<?php

namespace App\Http\Controllers;
class IndexController extends Controller
{
    // use AuthorizesRequests, DispatchesJobs, ValidatesRequests;
    public function Welcome()
    {
        // dd(session()->all());
        // dd($orders);

        session()->forget('usuario_dni');
        session()->forget('email');
        session()->forget('clave');
        session()->forget('nombres');
        return view('welcome');
    }
}