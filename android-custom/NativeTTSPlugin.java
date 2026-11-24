package com.marketdict.app;

import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.speech.tts.Voice;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import java.util.List;
import java.util.Locale;
import java.util.Set;

@CapacitorPlugin(name = "NativeTTS")
public class NativeTTSPlugin extends Plugin {
    private TextToSpeech tts;
    private boolean isInitialized = false;
    private PluginCall activeCall = null;

    @Override
    public void load() {
        initTTS(null);
    }

    private String findGoogleTtsEngine() {
        try {
            TextToSpeech probe = new TextToSpeech(getContext(), null);
            List<TextToSpeech.EngineInfo> engines = probe.getEngines();
            try { probe.shutdown(); } catch (Exception ignored) {}
            if (engines != null) {
                for (TextToSpeech.EngineInfo e : engines) {
                    if ("com.google.android.tts".equals(e.name)) {
                        return e.name;
                    }
                }
            }
        } catch (Exception ignored) {}
        return null;
    }

    private synchronized void initTTS(Runnable onReady) {
        if (tts != null && isInitialized) {
            if (onReady != null) onReady.run();
            return;
        }

        try {
            String engine = findGoogleTtsEngine();
            TextToSpeech.OnInitListener listener = status -> {
                if (status == TextToSpeech.SUCCESS) {
                    isInitialized = true;
                    setupUtteranceListener();
                    if (onReady != null) onReady.run();
                } else {
                    isInitialized = false;
                    if (onReady != null) onReady.run();
                }
            };

            if (engine != null) {
                tts = new TextToSpeech(getContext(), listener, engine);
            } else {
                tts = new TextToSpeech(getContext(), listener);
            }
        } catch (Exception e) {
            isInitialized = false;
            if (onReady != null) onReady.run();
        }
    }

    private void setupUtteranceListener() {
        if (tts == null) return;
        tts.setOnUtteranceProgressListener(new UtteranceProgressListener() {
            @Override
            public void onStart(String utteranceId) {}

            @Override
            public void onDone(String utteranceId) {
                resolveActiveCall(true);
            }

            @Override
            public void onError(String utteranceId) {
                resolveActiveCall(false);
            }

            @Override
            public void onStop(String utteranceId, boolean interrupted) {
                resolveActiveCall(false);
            }
        });
    }

    private synchronized void resolveActiveCall(boolean completed) {
        if (activeCall != null) {
            PluginCall call = activeCall;
            activeCall = null;
            try {
                JSObject ret = new JSObject();
                ret.put("completed", completed);
                call.resolve(ret);
            } catch (Exception ignored) {}
        }
    }

    @PluginMethod
    public void speak(PluginCall call) {
        String text = call.getString("text", "");
        String lang = call.getString("lang", "fa");
        Double rateVal = call.getDouble("rate", 1.0);
        float rate = rateVal != null ? rateVal.floatValue() : 1.0f;

        if (text == null || text.trim().isEmpty()) {
            JSObject ret = new JSObject();
            ret.put("completed", true);
            call.resolve(ret);
            return;
        }

        resolveActiveCall(false);

        if (tts == null || !isInitialized) {
            initTTS(() -> performSpeak(text, lang, rate, call));
        } else {
            performSpeak(text, lang, rate, call);
        }
    }

    private void performSpeak(String text, String lang, float rate, PluginCall call) {
        if (tts == null || !isInitialized) {
            JSObject ret = new JSObject();
            ret.put("completed", false);
            ret.put("error", "TTS_NOT_INITIALIZED");
            call.resolve(ret);
            return;
        }

        try {
            if ("en".equalsIgnoreCase(lang) || "en-US".equalsIgnoreCase(lang) || "en_US".equalsIgnoreCase(lang)) {
                tts.setLanguage(Locale.US);
            } else {
                // Persian language requested
                Locale faLocale = new Locale("fa", "IR");
                int res = tts.setLanguage(faLocale);
                if (res == TextToSpeech.LANG_NOT_SUPPORTED) {
                    res = tts.setLanguage(new Locale("fa"));
                }

                // Check voices list for any exact Persian voice matching (e.g. fa, fas, fa-ir)
                try {
                    Set<Voice> voices = tts.getVoices();
                    if (voices != null) {
                        for (Voice v : voices) {
                            Locale loc = v.getLocale();
                            if (loc != null) {
                                String code = loc.getLanguage();
                                if ("fa".equalsIgnoreCase(code) || "fas".equalsIgnoreCase(code) || "per".equalsIgnoreCase(code)) {
                                    tts.setVoice(v);
                                    tts.setLanguage(loc);
                                    res = TextToSpeech.LANG_AVAILABLE;
                                    break;
                                }
                            }
                        }
                    }
                } catch (Exception ignored) {}

                // If completely unsupported by the engine, notify JS cleanly
                if (res == TextToSpeech.LANG_NOT_SUPPORTED) {
                    JSObject ret = new JSObject();
                    ret.put("completed", false);
                    ret.put("error", "PERSIAN_NOT_SUPPORTED");
                    call.resolve(ret);
                    return;
                }
            }

            tts.setSpeechRate(Math.max(0.6f, Math.min(2.0f, rate)));
            activeCall = call;
            String utteranceId = "utterance_" + System.currentTimeMillis();
            tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, utteranceId);
        } catch (Exception e) {
            resolveActiveCall(false);
            call.reject("Native TTS error: " + e.getMessage());
        }
    }

    @PluginMethod
    public void stop(PluginCall call) {
        resolveActiveCall(false);
        if (tts != null) {
            try {
                tts.stop();
            } catch (Exception ignored) {}
        }
        JSObject ret = new JSObject();
        ret.put("stopped", true);
        call.resolve(ret);
    }

    @Override
    protected void handleOnDestroy() {
        if (tts != null) {
            try {
                tts.stop();
                tts.shutdown();
            } catch (Exception ignored) {}
            tts = null;
        }
        super.handleOnDestroy();
    }
}
